from threading import Thread, Lock, Event
from queue import Queue, Empty
from select import select
from socket import socket
import socket as s
from typing import List, Optional, Callable
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import SECP256k1
from Cryptodome.Cipher import AES
from Cryptodome.Cipher._mode_gcm import GcmMode
from Cryptodome.Random import get_random_bytes
from binascii import a2b_hex, b2a_hex
from hashlib import sha256
import json
import zlib

try:
    from . import SecureReliableSocket
except (ImportError, ModuleNotFoundError):
    from srudp import SecureReliableSocket

# typing
CallbackFnc = Callable[[bytes, 'Sock'], None]

# flags
F_ENCRYPTED = 0b00000001
F_COMPRESSED = 0b00000010
F_VALIDATED = 0b00000100
F_INNER_WORK = 0b0001000
F_IS_CLOSING = 0b10000000
IS_SERVER = True
IS_CLIENT = False
D_INBOUND = "inbound"
D_OUTBOUND = "outbound"
D_BIBOUND = "bibound"

# shared key's curve
CURVE = SECP256k1


class UnrecoverableError(Exception):
    """data processing has collapsed and socket is closed"""


class JobCorruptedWarning(Warning):
    """a job was damaged in the process and socket is returned to listen state"""


class Sock(object):
    """client socket object wrapper and callback"""

    def __init__(
            self,
            sock: socket,
            callback: CallbackFnc,
            server: bool,
            public_key: VerifyingKey,
    ):
        assert sock.gettimeout() is False, "sock is no blocking mode"
        self.sock = sock
        self.lock = Lock()
        self.callback = callback
        # note: check inner work is processing by inner_que is None or not
        self.inner_que: Optional[Queue[bytes]] = None
        self.inner_event: Optional[Event] = None
        self.is_server = server
        self.tmp = bytearray()
        self.common_key: Optional[bytes] = None
        self.public_key: VerifyingKey = public_key
        self.flags = 0b00000000  # default no flag

    @staticmethod
    def _encrypt(key: bytes, data: bytes) -> bytes:
        """encrypt by AES-GCM (more secure than CBC mode)"""
        cipher: 'GcmMode' = AES.new(key, AES.MODE_GCM)  # type: ignore
        # warning: Don't reuse nonce
        enc, tag = cipher.encrypt_and_digest(data)
        # output length = 16bytes + 16bytes + N(=data)bytes
        return cipher.nonce + tag + enc

    @staticmethod
    def _decrypt(key: bytes, data: bytes) -> bytes:
        """decrypt by AES-GCM (more secure than CBC mode)"""
        cipher: 'GcmMode' = AES.new(key, AES.MODE_GCM, nonce=data[:16])  # type: ignore
        # ValueError raised when verify failed
        try:
            return cipher.decrypt_and_verify(data[32:], data[16:32])
        except ValueError:
            pass
        raise UnrecoverableError("decryption failed")

    def recv(self) -> None:
        """push new raw bytes and find new chunk msg"""
        assert not self.is_server
        try:
            data = self.sock.recv(4096)
        except BlockingIOError:
            return
        if len(data) == 0:
            raise UnrecoverableError("receive zero message (socket is closed)")
        self.tmp.extend(data)
        flag = self.tmp[0]
        length = int.from_bytes(self.tmp[1:5], "little")

        if len(self.tmp) < 5 + length:
            return  # not found new msg
        else:
            # find new chunked msg
            raw = self.tmp[5:5 + length]
            self.tmp: bytearray = self.tmp[5 + length:]

            # revert
            if flag & F_ENCRYPTED:
                if self.common_key is None:
                    raise UnrecoverableError("try to decrypt msg but not found key")
                else:
                    raw = self._decrypt(self.common_key, raw)
            if flag & F_COMPRESSED:
                raw = zlib.decompress(raw)
            msg = bytes(raw)

            # execute callback with same thread
            # warning: don't block because a listen thread fall in dysfunctional
            if flag % F_INNER_WORK:
                if self.inner_que is None:
                    # start inner work thread
                    self.ignite_inner_work(msg)
                else:
                    self.inner_que.put(msg)
            elif flag & F_IS_CLOSING:
                # closing request
                raise UnrecoverableError(f"closing request: {msg.decode(errors='ignore')}")
            else:
                # is outer work
                self.callback(msg, self)
            return

    def sendall(self, msg: bytes, flag: int = None) -> None:
        """send chunked message"""
        assert not self.is_server

        # manual setup flag
        if flag is None:
            flag = self.flags

        # convert
        if flag & F_COMPRESSED:
            msg = zlib.compress(msg)
        if flag & F_ENCRYPTED:
            if self.common_key is None:
                raise JobCorruptedWarning("try to encrypt msg but not found key")
            else:
                msg = self._encrypt(self.common_key, msg)

        with self.lock:
            # convert: [flag 1b][len 4b][msg xb]
            self.sock.sendall(flag.to_bytes(1, "little") + len(msg).to_bytes(4, "little") + msg)

    def ignite_inner_work(self, msg: bytes) -> None:
        """start inner work thread by F_INNER_WORK"""
        assert self.inner_que is None
        obj: dict = json.loads(msg.decode())

        if "ignite" not in obj:
            raise JobCorruptedWarning("no ignite flag and no inner work")

        elif obj["ignite"] == "encryption":
            self.establish_encryption(False)
            assert self.inner_que is not None
            self.inner_que.put(msg)

        elif obj["ignite"] == "validation":
            self.validate_the_other(False, None)

        else:
            raise NotImplementedError(f"unknown ignite flag: {obj}")

    def establish_encryption(self, is_primary: bool) -> None:
        """establish encrypted connection"""
        assert isinstance(self.common_key, bytes), "already established encryption (key)"
        assert not (self.flags & F_ENCRYPTED), "already established encryption (flag)"
        assert self.inner_que is None and self.inner_event is None

        # check result by `self.flags & F_ENCRYPTED is True`
        recv_que: 'Queue[bytes]' = Queue()
        finished_event = Event()
        finished_event.clear()

        def send_json(obj: dict) -> None:
            """send inner work msg by plain"""
            self.sendall(json.dumps(obj).encode() + b"\n", F_INNER_WORK)

        def recv_json() -> dict:
            """recv inner work msg or raise queue.Empty"""
            return json.loads(recv_que.get(True, 5.0).decode())

        def close_inner() -> None:
            """close inner process"""
            self.inner_que = None
            self.inner_event = None
            finished_event.set()

        def inner_work() -> None:
            common_key: Optional[bytes] = None
            shared_key: Optional[bytes] = None
            established_msg = b"success establish encrypted connection"

            try:
                # first stage
                if is_primary:
                    # (primary): generate pair, send pk & curve
                    my_sk = SigningKey.generate(CURVE)
                    my_pk: VerifyingKey = my_sk.get_verifying_key()
                    send_json({
                        "ignite": "encryption",
                        "curve": str(CURVE.name),
                        "public-key": my_pk.to_string().hex()
                    })
                else:
                    # (standby): receive pk, calc sharedKey, send
                    my_sk = SigningKey.generate(CURVE)
                    my_pk: VerifyingKey = my_sk.get_verifying_key()
                    obj = recv_json()
                    assert str(obj.get("curve")) == CURVE.name, "{} is not same curve".find(obj.get("curve"))
                    assert "public-key" in obj
                    other_pk = VerifyingKey.from_string(a2b_hex(obj["public-key"]))
                    shared_point = my_sk.privkey.secret_multiplier * other_pk.pubkey.point
                    shared_key = sha256(shared_point.x().to_bytes(32, 'big')).digest()
                    common_key = get_random_bytes(32)
                    encrypted_key = self._encrypt(shared_key, common_key)
                    send_json({
                        "public-key": my_pk.to_string().hex(),
                        "encrypted-key": encrypted_key.hex()
                    })

                # second stage
                if is_primary:
                    # (primary): receive pk & encryptedKey, calc sharedKey
                    # decrypt commonKey, send hell msg
                    obj = recv_json()
                    assert "public-key" in obj
                    other_pk = VerifyingKey.from_string(a2b_hex(obj["public-key"]))
                    shared_point = my_sk.privkey.secret_multiplier * other_pk.pubkey.point
                    shared_key = sha256(shared_point.x().to_bytes(32, 'big')).digest()
                    assert "encrypted-key" in obj
                    common_key = self._decrypt(shared_key, a2b_hex(obj["encrypted-key"]))
                    encrypted_msg = self._encrypt(shared_key, established_msg)
                    send_json({
                        "encrypted-msg": encrypted_msg.hex()
                    })
                else:
                    # (standby): receive encrypted msg, confirm connection by decrypting
                    obj = recv_json()
                    assert "encrypted-msg" in obj
                    assert isinstance(shared_key, bytes)
                    msg = self._decrypt(shared_key, a2b_hex(obj["encrypted-msg"]))
                    assert msg == established_msg

                # something is wrong on negotiation
            except Empty:
                pass
            except AssertionError as e:
                print("AssertionError", e)
            except Exception:
                import traceback
                traceback.print_exc()
            else:
                # success
                with self.lock:
                    self.common_key = common_key
                    self.flags |= F_ENCRYPTED
            finally:
                close_inner()

        # start background thread
        self.inner_que = recv_que
        self.inner_event = finished_event
        Thread(target=inner_work, name="InnerEnc").start()

    def validate_the_other(self, is_primary: bool, other_pk: bytes = None) -> None:
        """validate the other by publicKey"""
        assert self.inner_que is None and self.inner_event is None

        # check result by `self.flags & F_ENCRYPTED is True`
        recv_que: 'Queue[bytes]' = Queue()
        finished_event = Event()
        finished_event.clear()

        def send_json(obj: dict) -> None:
            """send inner work msg by plain"""
            self.sendall(json.dumps(obj).encode() + b"\n", F_INNER_WORK)

        def recv_json() -> dict:
            """recv inner work msg or raise queue.Empty"""
            return json.loads(recv_que.get(True, 5.0).decode())

        def close_inner() -> None:
            """close inner process"""
            self.inner_que = None
            self.inner_event = None
            finished_event.set()

        def inner_work() -> None:
            # TODO: なにか
            # success
            with self.lock:
                self.flags |= F_VALIDATED

        self.inner_que = recv_que
        self.inner_event = finished_event
        Thread(target=inner_work, name="InnerVal").start()

    def fileno(self) -> int:
        """is for select poll"""
        return self.sock.fileno()

    def close(self) -> None:
        """only call once"""
        self.sock.close()


class SockPool(Thread):
    """"""

    def __init__(self, name: str = None, secret: bytes = None) -> None:
        super().__init__(name=name)
        self.socks: List[Sock] = list()
        self.lock = Lock()
        if secret is None:
            self.secret = SigningKey.generate(CURVE)
        else:
            self.secret = SigningKey.from_string(secret, CURVE)
        self.public = self.secret.get_verifying_key()
        # status
        self.running = Event()  # main thread is working
        self.closing = False  # is closing now
        self.closed = False  # class is closed
        self.error = None
        # init
        self.running.set()

    def run(self) -> None:
        assert self.running.is_set(), "already running main thread"
        self.running.clear()

        # listen sockets
        while not self.closing:
            # note: only socket object is supported
            with self.lock:
                r, _w, _x = select(self.socks, [], [], 0.2)
            r: List[Sock]

            # socket recv() or accept()
            for sock in r:
                if sock.is_server:
                    raw_sock, _addr = sock.sock.accept()
                    new_sock = Sock(raw_sock, sock.callback, IS_CLIENT, self.public)
                    with self.lock:
                        self.socks.append(new_sock)
                else:
                    try:
                        sock.recv()
                    except UnrecoverableError as e:
                        print("UnrecoverableError", sock, e)
                        self.close_sock(sock)
                    except ConnectionError as e:
                        print("ConnectionError", sock, e)
                        self.close_sock(sock)
                    except NotImplementedError as e:
                        print("NotImplementedError", sock, e)
                    except JobCorruptedWarning as e:
                        print("JobCorruptedWarning", sock, e)
                    except Exception:
                        import traceback
                        traceback.print_exc()
                        self.close_sock(sock)

        # close is signaled
        self.running.set()

    def start_tcp_server(self, port: int, callback: CallbackFnc) -> None:
        """listen new TCP server"""
        sock = socket(s.AF_INET, s.SOCK_STREAM)
        sock.bind(("", port))
        sock.listen(20)
        sock.setblocking(False)

        # listen server sock
        with self.lock:
            # TODO: encrypt compress は 後に有効にする
            self.socks.append(Sock(sock, callback, IS_SERVER, self.public))

    def start_tcp_client(self, address: tuple, callback: CallbackFnc) -> None:
        """start new TCP client connection"""
        sock = socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect(address)
        sock.setblocking(False)

        # listen new data receive
        with self.lock:
            self.socks.append(Sock(sock, callback, IS_CLIENT, self.public))

    def connect_tcp(self, address):
        """"""
        # 1. connect TCP socket
        sock = socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect(address)

        # 2. send my public key
        sock.sendall(json.dumps({
            "curve": CURVE.name,
            "public-key": self.public.to_string().hex(),
        }).encode() + b"\n")

        # 3. receive other's public key and encrypted key
        obj: dict = json.loads(sock.recv(2048))
        assert obj.get("curve") == CURVE.name
        other_public = VerifyingKey.from_string(a2b_hex(obj.get("public-key")), CURVE)

        # 4. calc tmp key
        point = self.secret.privkey.secret_multiplier * other_public.pubkey.point
        encrypt_key = sha256(point.x().to_bytes(32, 'big')).digest()

        # 5. decrypt encrypted key

        # 1. generate shared key
        shared_key = get_random_bytes(32)

        # 2. encrypt send my public key

    def close_sock(self, sock: Sock, reason: bytes = None) -> None:
        """graceful socket close"""
        try:
            # send reason if socket is working
            if isinstance(reason, bytes):
                sock.sendall(reason, F_IS_CLOSING)
            # close socket is living yet
            if sock.fileno() != -1:
                sock.close()
        except ConnectionError as e:
            print("ConnectionError", e)
        except Exception:
            import traceback
            traceback.print_exc()

        # remove from list
        with self.lock:
            if sock in self.socks:
                self.socks.remove(sock)

    def close(self) -> None:
        """close and wait complete status"""
        self.closing = True
        self.running.wait()
        self.closed = True


import asyncio


__all__ = [
    "CallbackFnc",
    "Sock",
    "SockPool",
]
