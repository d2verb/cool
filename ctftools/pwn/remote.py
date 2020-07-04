import socket
import telnetlib
import time
from typing import Optional

from ctftools.util.enc import b2s
from termcolor import colored


class Remote:
    def __init__(self, host: str, port: int, timeout: Optional[int] = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.conn = socket.create_connection((self.host, self.port))

    def close(self):
        self.conn.close()

    def interact(self):
        t = telnetlib.Telnet()
        t.sock = self.conn

        # Telnet.interact() will call text.decode("ascci") but this will fail sometimes.
        # We just print bytes itself for avoiding UnicodeDecodeError.
        while True:
            try:
                time.sleep(1)

                inp = b2s(t.read_very_eager())
                print(inp, end="")

                out = input(colored(">> ", "green"))
                t.write(out.encode("utf8") + b"\n")
            except EOFError:
                break

    def recv(self, numb: int = 4096, timeout: Optional[int] = None) -> bytes:
        self.__settimeout(self.timeout)
        data = self.conn.recv(numb)
        return data

    def recvuntil(
        self, delim: bytes, timeout: Optional[int] = None, drop: bool = False
    ) -> bytes:
        data = b""
        while data[-len(delim) :] != delim:
            data += self.recv(1, timeout=timeout)
        if drop:
            data = data[: -len(delim)]
        return data

    def send(self, data: bytes, timeout: Optional[int] = None):
        self.__settimeout(timeout)
        self.conn.sendall(data)

    def sendafter(self, data: bytes, delim: bytes, timeout: Optional[int] = None):
        self.recvuntil(delim, timeout=timeout)
        self.send(data, timeout=timeout)

    def sendline(
        self, data: bytes, newline: bytes = b"\n", timeout: Optional[int] = None
    ):
        self.send(data + newline, timeout=timeout)

    def sendlineafter(
        self,
        data: bytes,
        delim: bytes,
        newline: bytes = b"\n",
        timeout: Optional[int] = None,
    ):
        self.recvuntil(delim, timeout=timeout)
        self.sendline(data, newline=newline, timeout=timeout)

    def __settimeout(self, timeout: Optional[int] = None):
        if timeout is None:
            self.conn.settimeout(self.timeout)
        else:
            self.conn.settimeout(timeout)


def remote(host: str, port: int, timeout: Optional[int] = None) -> Remote:
    return Remote(host, port, timeout=timeout)
