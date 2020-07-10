import socket
import telnetlib
import time
from typing import Optional

from termcolor import colored

from cool.util import b2s


class Remote:
    """Class for connecting to a remote server.

    :param host: host name of the server
    :param port: port number of the server
    :param timeout: timeout in seconds
    """
    def __init__(self, host: str, port: int, timeout: Optional[int] = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.conn = socket.create_connection((self.host, self.port))

    def close(self) -> None:
        """Close the connection.
        """
        self.conn.close()

    def interact(self) -> None:
        """Launch the interactive shell to the server.
        """
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
        """Receive data from the server.

        :param numb: maximum data size to receive
        :param timeout: timeout in seconds
        :return: received data
        """
        self.__settimeout(timeout)
        data = self.conn.recv(numb)
        return data

    def recvuntil(
        self, delim: bytes, timeout: Optional[int] = None, drop: bool = False
    ) -> bytes:
        """Receive data from the server until hitting the delimiter.

        :param delim: the delimiter
        :param timeout: timeout in seconds
        :param drop: drop the delimiter or not
        :return: received data with/without delimiter
        """
        data = b""
        while data[-len(delim) :] != delim:
            data += self.recv(1, timeout=timeout)
        if drop:
            data = data[: -len(delim)]
        return data

    def send(self, data: bytes, timeout: Optional[int] = None) -> None:
        """Send data to the server.

        :param data: data to send
        :param timeout: timeout in seconds
        """
        self.__settimeout(timeout)
        self.conn.sendall(data)

    def sendafter(self, delim: bytes, data: bytes, timeout: Optional[int] = None) -> None:
        """Send data to the server after receiving delimiter.

        :param delim: the delimiter
        :param data: data to send
        :param timeout: timeout in seconds
        """
        self.recvuntil(delim, timeout=timeout)
        self.send(data, timeout=timeout)

    def sendline(
        self, data: bytes, newline: bytes = b"\n", timeout: Optional[int] = None
    ) -> None:
        """Send data with newline character.

        :param data: data to send
        :param newline: newline character
        :param timeout: timeout in seconds
        """
        self.send(data + newline, timeout=timeout)

    def sendlineafter(
        self,
        delim: bytes,
        data: bytes,
        newline: bytes = b"\n",
        timeout: Optional[int] = None,
    ) -> None:
        """Send data with newline character after receiving delimiter.

        :param data: data to send
        :param delim: the delimiter
        :param newline: newline character
        :param timeout: timeout in seconds
        """
        self.recvuntil(delim, timeout=timeout)
        self.sendline(data, newline=newline, timeout=timeout)

    def __settimeout(self, timeout: Optional[int] = None) -> None:
        if timeout is None:
            self.conn.settimeout(self.timeout)
        else:
            self.conn.settimeout(timeout)


def remote(host: str, port: int, timeout: Optional[int] = None) -> Remote:
    """Create a remote connection the server.

    :param host: host name of the server
    :param port: port number of the server
    :param timeout: timeout in seconds
    """
    return Remote(host, port, timeout=timeout)
