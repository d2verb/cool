from ctftools.utils import b64enc, b64dec


def test_b64enc():
    assert b64enc(b"Lorem Ipsum") == b"TG9yZW0gSXBzdW0="


def test_b64dec():
    assert b64dec(b"TG9yZW0gSXBzdW0=") == b"Lorem Ipsum"
