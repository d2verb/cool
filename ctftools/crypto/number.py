import logging
from collections import defaultdict
from math import gcd
from random import randint
from typing import DefaultDict, Optional, Tuple

from Crypto.Util.number import bytes_to_long, long_to_bytes

logger = logging.getLogger(__name__)


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


def pollard_rho(n: int, seed: int = 3) -> Optional[int]:
    def f(x):
        return seed * x + 1

    x, y, d = 2, 2, 1

    while d == 1:
        x = f(x) % n
        y = f(f(y)) % n
        d = gcd(abs(x - y), n)

    if d != n:
        return d

    return None


def prime_factorization(n: int) -> DefaultDict[int, int]:
    factors: DefaultDict[int, int] = defaultdict(lambda: 0)

    logger.debug(f"start prime factorizing {n} ...")
    while n != 1:
        if miller_rabin_test(n):
            factors[n] += 1
            logger.debug(f"found prime factor: {n}")
            n //= n
        else:
            for seed in [3, 5, 7, 11, 13, 17]:
                f = pollard_rho(n, seed=seed)
                if f is not None:
                    break
            else:
                raise Exception(f"can't find factor of {n}")

            if miller_rabin_test(f):
                factors[f] += 1
                logger.debug(f"found prime factor: {f}")
            else:
                f_factors = prime_factorization(f)
                for p, q in f_factors.items():
                    factors[p] += q

            n //= f

    return factors
