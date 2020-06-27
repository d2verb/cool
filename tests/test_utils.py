from ctftools.utils import b64enc, b64dec


def test_b64enc():
    inp = b"Lorem Ipsum"
    out = b"TG9yZW0gSXBzdW0="
    assert b64enc(inp) == out


def test_b64dec():
    inp = b"TG9yZW0gSXBzdW0="
    out = b"Lorem Ipsum"
    assert b64dec(inp) == out
