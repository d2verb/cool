from base64 import b64encode, b64decode


def b64enc(s: bytes) -> bytes:
    return b64encode(s)


def b64dec(s: bytes) -> bytes:
    return b64decode(s)
