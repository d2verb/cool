import socket
import telnetlib
import time
from typing import Optional

from termcolor import colored

from cool.util import b2s

from .tube import Tube


class Remote(Tube):
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

        # "Telnet" HAS "sock" ATTRIBUTE!!
        t.sock = self.conn  # type: ignore

        # Telnet.interact() will call text.decode("ascci") but this will fail sometimes.
        # We just print bytes itself for avoiding UnicodeDecodeError.
        while True:
            try:
                time.sleep(0.5)

                inp = b2s(t.read_very_eager())
                print(inp)

                out = input(colored(">> ", "green"))
                t.write(out.encode("utf8") + b"\n")
            except (EOFError, BrokenPipeError):
                break

    def recv(self, numb: int = 4096, timeout: Optional[int] = None) -> bytes:
        """Receive data from the server.

        :param numb: maximum data size to receive
        :param timeout: timeout in seconds
        :return: received data
        """
        self.__settimeout(timeout)
        try:
            data = self.conn.recv(numb)
        except socket.timeout:
            raise TimeoutError
        return data

    def send(self, data: bytes, timeout: Optional[int] = None) -> None:
        """Send data to the server.

        :param data: data to send
        :param timeout: timeout in seconds
        """
        self.__settimeout(timeout)
        try:
            self.conn.sendall(data)
        except socket.timeout:
            raise TimeoutError

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
