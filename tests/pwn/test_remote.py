from unittest import mock

from ctftools.pwn import remote


class ConnectionMock:
    def __init__(self):
        self.idx = 0
        self.msg = b"this is line1\nthis is line2\nthis is line3\nthis is line4"

    def recv(self, numb: int) -> bytes:
        result = self.msg[self.idx : self.idx + numb]
        self.idx += numb
        return result


class TestRemote:
    def setup_method(self):
        self.conn = ConnectionMock()
        self.conn.sendall = mock.MagicMock(name="sendall")
        self.conn.settimeout = mock.MagicMock(name="settimeout")

    def test_recv(self):
        with mock.patch("socket.create_connection", return_value=self.conn):
            r = remote("example.com", 12345)

            # test recvuntil()
            assert r.recvuntil(b"\n") == b"this is line1\n"
            assert r.recvuntil(b"\n", drop=True) == b"this is line2"

            # test recv()
            assert r.recv(5) == b"this "
            assert r.recv() == b"is line3\nthis is line4"

    def test_send(self):
        with mock.patch("socket.create_connection", return_value=self.conn):
            r = remote("example.com", 12345)

            # test send()
            r.send(b"sample input 1")
            r.conn.sendall.assert_called_with(b"sample input 1")

            # test sendafter()
            r.sendafter(b"sample input 2", delim=b"line2\n")
            r.conn.sendall.assert_called_with(b"sample input 2")
            assert r.recvuntil(b"\n") == b"this is line3\n"

            # test sendline()
            r.sendline(b"sample input 3")
            r.conn.sendall.assert_called_with(b"sample input 3\n")
