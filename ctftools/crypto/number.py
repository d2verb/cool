from typing import Tuple

from Crypto.Util.number import bytes_to_long, long_to_bytes


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a: int, m: int) -> int:
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


def btoi(b: bytes) -> int:
    return bytes_to_long(b)


def itob(i: int) -> bytes:
    return long_to_bytes(i)
