import codecs
import sys


def rot13(s: str) -> str:
    return codecs.encode(s, "rot13")


def xorcipher(bs: bytes, key: bytes) -> bytes:
    result = bytes()
    for i, b in enumerate(bs):
        b = b ^ key[i % len(key)]  # if len(bs) > len(key), repeat key
        result += b.to_bytes(1, byteorder=sys.byteorder)
    return result
