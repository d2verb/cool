import os
import signal
import time
from contextlib import contextmanager
from subprocess import PIPE, Popen
from typing import Optional

from termcolor import colored

from cool.util import b2s

from .tube import Tube


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


class Process(Tube):
    """Class for interacting with program process.

    :param path: the program path
    :param timeout: timeout in seconds
    """

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

    def send(self, data: bytes, timeout: Optional[int] = None) -> None:
        if timeout is None:
            timeout = self.timeout

        # self.conn.stdin must be not-None because the stdout argument of Popen was PIPE.
        # So we ignore mypy's error at this point.
        with timelimit(timeout):
            self.conn.stdin.write(data)  # type: ignore
            self.conn.stdin.flush()  # type: ignore


def process(path: str, timeout: Optional[int] = None) -> Process:
    """Create a interaction for the process.

    :param path: the path of program
    :param timeout: timeout in seconds
    """
    return Process(path, timeout=timeout)
