from abc import abstractmethod
from typing import Optional, Protocol


class Tube(Protocol):
    @abstractmethod
    def recv(self, numb: int = 4096, timeout: Optional[int] = None) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def send(self, data: bytes, timeout: Optional[int] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def interact(self) -> None:
        raise NotImplementedError

    def recvuntil(
        self, delim: bytes, timeout: Optional[int] = None, drop: bool = False
    ) -> bytes:
        """Receive data until hitting the delimiter.

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

    def sendafter(
        self, delim: bytes, data: bytes, timeout: Optional[int] = None
    ) -> None:
        """Send data after receiving delimiter.

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
