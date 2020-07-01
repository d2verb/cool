from base64 import b64decode, b64encode
from typing import Union
from urllib.parse import quote, unquote


def b64enc(bs: bytes) -> bytes:
    return b64encode(bs)


def b64dec(bs: bytes) -> bytes:
    return b64decode(bs)


def urlenc(string: Union[str, bytes]) -> str:
    return quote(string)


def urldec(string: str) -> str:
    return unquote(string)
