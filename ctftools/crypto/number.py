from math import gcd
from random import randint
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


def fermat_test(n: int, k: int = 100) -> bool:
    if n in [1, 2]:
        return [False, True][n - 1]

    for _ in range(k):
        a = randint(2, n - 1)

        if gcd(n, a) != 1:
            return False

        if pow(a, n - 1, n) != 1:
            return False

    return True


def miller_rabin_test(n: int, k: int = 30) -> bool:
    if n in [1, 2]:
        return [False, True][n - 1]

    s, d = 0, n - 1

    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = randint(2, n - 1)
        x = pow(a, d, n)

        for r in range(s):
            if x == n - 1 or x == 1:
                break
            x = (x * x) % n
        else:
            return False

    return True
