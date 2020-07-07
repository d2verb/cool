from cool.util.enc import b64dec, b64enc, urldec, urlenc


def test_b64enc():
    assert b64enc(b"Lorem Ipsum") == b"TG9yZW0gSXBzdW0="

    # test urlsafe mode
    assert b64enc(b"\xf8\xff\xff") == b"+P//"
    assert b64enc(b"\xf8\xff\xff", url=True) == b"-P__"


def test_b64dec():
    assert b64dec(b"TG9yZW0gSXBzdW0=") == b"Lorem Ipsum"

    # test urlsafe mode
    assert b64dec(b"+P//") == b"\xf8\xff\xff"
    assert b64dec(b"-P__", url=True) == b"\xf8\xff\xff"


def test_urlenc():
    assert urlenc("/El Niño/") == "/El%20Ni%C3%B1o/"
    assert urlenc("/El Niño/".encode("utf-8")) == "/El%20Ni%C3%B1o/"


def test_urldec():
    assert urldec("/El%20Ni%C3%B1o/") == "/El Niño/"
