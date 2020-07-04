from unittest import mock

from ctftools.pwn.tube import Tube


class ConnectionMock:
    def __init__(self):
        self.idx = 0
        self.msg = b"this is line1\nthis is line2\nthis is line3\nthis is line4"

    def recv(self, numb: int) -> bytes:
        result = self.msg[self.idx : self.idx + numb]
        self.idx += numb
        return result


class TestPwn:
    def setup_method(self):
        self.conn = ConnectionMock()
        self.conn.sendall = mock.MagicMock(name="sendall")
        self.conn.settimeout = mock.MagicMock(name="settimeout")

    def test_recv(self):
        with mock.patch("socket.create_connection", return_value=self.conn):
            t = Tube("example.com", 12345)

            # test recvuntil()
            assert t.recvuntil(b"\n") == b"this is line1\n"
            assert t.recvuntil(b"\n", drop=True) == b"this is line2"

            # test recv()
            assert t.recv(5) == b"this "
            assert t.recv() == b"is line3\nthis is line4"

    def test_send(self):
        with mock.patch("socket.create_connection", return_value=self.conn):
            t = Tube("example.com", 12345)

            # test send()
            t.send(b"sample input 1")
            t.conn.sendall.assert_called_with(b"sample input 1")

            # test sendafter()
            t.sendafter(b"sample input 2", delim=b"line2\n")
            t.conn.sendall.assert_called_with(b"sample input 2")
            assert t.recvuntil(b"\n") == b"this is line3\n"

            # test sendline()
            t.sendline(b"sample input 3")
            t.conn.sendall.assert_called_with(b"sample input 3\n")
