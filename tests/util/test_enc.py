from ctftools.util.enc import b64dec, b64enc, urldec, urlenc


def test_b64enc():
    assert b64enc(b"Lorem Ipsum") == b"TG9yZW0gSXBzdW0="


def test_b64dec():
    assert b64dec(b"TG9yZW0gSXBzdW0=") == b"Lorem Ipsum"


def test_urlenc():
    assert urlenc("/El Niño/") == "/El%20Ni%C3%B1o/"
    assert urlenc("/El Niño/".encode("utf-8")) == "/El%20Ni%C3%B1o/"


def test_urldec():
    assert urldec("/El%20Ni%C3%B1o/") == "/El Niño/"
