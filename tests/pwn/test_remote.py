import socket

from cool.pwn import remote


def test_remote():
    r = remote("www.example.com", 80)

    # send request
    r.sendline(b"GET / HTTP/1.1\r")
    r.send(b"Host: www.example.com\r\n\r\n")

    # receive status line
    status_line = r.recvuntil(b"\r\n", drop=True)
    assert status_line == b"HTTP/1.1 200 OK"

    # receive rest of the response
    response = r.recv()
    assert len(response) > 0

    # TODO: Web should test sendafter() but how...

    r.close()


def test_timeout():
    # passing the timeout parameter as a method argument
    r = remote("www.example.com", 80)
    timed_out = False
    try:
        r.recvuntil(b"meme", timeout=1)
    except TimeoutError:
        timed_out = True
    except Exception:
        pass
    finally:
        r.close()
    assert timed_out

    # passing the timeout parameter as a constructor argument
    r = remote("www.example.com", 80, timeout=1)
    timed_out = False
    try:
        r.recvuntil(b"meme")
    except TimeoutError:
        timed_out = True
    except Exception:
        pass
    finally:
        r.close()
    assert timed_out
