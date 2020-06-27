from base64 import b64decode, b64encode


def b64enc(bs: bytes) -> bytes:
    return b64encode(bs)


def b64dec(bs: bytes) -> bytes:
    return b64decode(bs)
