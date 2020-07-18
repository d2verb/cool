import os
import signal
import time
from contextlib import contextmanager
from subprocess import PIPE, Popen
from typing import Optional

from termcolor import colored

from cool.util import b2s


@contextmanager
def timelimit(timeout: Optional[int] = None):
    def sighdlr(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, sighdlr)
    signal.alarm(timeout if timeout else 0)
    try:
        yield
    finally:
        signal.alarm(0)


class Process:
    def __init__(self, path: str, timeout: Optional[int] = None) -> None:
        self.timeout = timeout
        self.path = os.path.abspath(path)
        self.conn = Popen(self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    def close(self) -> None:
        """Close the connection.
        """
        self.conn.terminate()

    def interact(self) -> None:
        """Launch the interactive shell.
        """
        while True:
            try:
                time.sleep(1)

                inp = b2s(self.recv())
                print(inp, end="")

                out = input(colored(">> ", "green"))
                self.sendline(out.encode("utf8"))
            except EOFError:
                break

    def recv(self, numb: int = 4096, timeout: Optional[int] = None) -> bytes:
        if timeout is None:
            timeout = self.timeout

        # self.conn.stdout must be not-None because the stdout argument of Popen was PIPE.
        # So we ignore mypy's error at this point.
        with timelimit(timeout):
            return self.conn.stdout.read1(numb)  # type: ignore

    def recvuntil(
        self, delim: bytes, timeout: Optional[int] = None, drop: bool = False
    ) -> bytes:
        """Receive data from the process until hitting the delimiter.

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
        if timeout is None:
            timeout = self.timeout

        # self.conn.stdin must be not-None because the stdout argument of Popen was PIPE.
        # So we ignore mypy's error at this point.
        with timelimit(timeout):
            self.conn.stdin.write(data)  # type: ignore
            self.conn.stdin.flush()  # type: ignore

    def sendafter(
        self, delim: bytes, data: bytes, timeout: Optional[int] = None
    ) -> None:
        """Send data to the process after receiving delimiter.

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


def process(path: str, timeout: Optional[int] = None) -> Process:
    """Create a connection to the process.

    :param path: the path of program
    :param timeout: timeout in seconds
    """
    return Process(path, timeout=timeout)
