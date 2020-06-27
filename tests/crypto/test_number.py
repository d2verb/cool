from random import randint

from ctftools.crypto.number import (
    btoi,
    egcd,
    fermat_test,
    itob,
    miller_rabin_test,
    modinv,
    prime_factorization,
)


def test_egcd():
    test_cases = [(23894798501898, 23948178468116), (1, 1), (12, 8)]
    for a, b in test_cases:
        (g, x, y) = egcd(a, b)
        assert a * x + b * y == g


def test_modinv():
    test_cases = [(3, 11), (31, 5), (3101, 51)]
    for a, m in test_cases:
        b = modinv(a, m)
        assert (a * b) % m == 1


def test_btoi():
    b = b"this is secret!"
    i = 604424160775843504266020346055193633
    assert btoi(b) == i


def test_itob():
    b = b"this is secret!"
    i = 604424160775843504266020346055193633
    assert itob(i) == b


def test_fermat_test():
    test_cases = [
        (1, False),
        (2, True),
        (3, True),
        (11, True),
        (31, True),
        (40, False),
        (41, True),
        (42, False),
        (43, True),
        (47, True),
        (311, True),
        (313, True),
        (314, False),
    ]

    for n, judge in test_cases:
        assert fermat_test(n) == judge


def test_miller_rabin_test():
    test_cases = [
        (1, False),
        (2, True),
        (3, True),
        (11, True),
        (31, True),
        (40, False),
        (41, True),
        (42, False),
        (43, True),
        (47, True),
        (311, True),
        (313, True),
        (314, False),
    ]

    for n, judge in test_cases:
        assert miller_rabin_test(n) == judge


def test_prime_factorization():
    for _ in range(5):
        n = randint(1, int(1e15))
        factors = prime_factorization(n)

        _n = 1
        for p, q in factors.items():
            assert miller_rabin_test(p)
            _n *= pow(p, q)

        assert _n == n
