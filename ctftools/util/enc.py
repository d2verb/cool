from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
from typing import Union
from urllib.parse import quote, unquote


def b64enc(bs: bytes, url: bool = False) -> bytes:
    if url:
        return urlsafe_b64encode(bs)
    else:
        return b64encode(bs)


def b64dec(bs: bytes, url: bool = False) -> bytes:
    if len(bs) % 4 != 0:
        bs += b"=" * (len(bs) % 4)

    if url:
        return urlsafe_b64decode(bs)
    else:
        return b64decode(bs)


def urlenc(string: Union[str, bytes]) -> str:
    return quote(string)


def urldec(string: str) -> str:
    return unquote(string)


def b2s(bs: bytes) -> str:
    return "".join(list(map(chr, bs)))
