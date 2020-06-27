from ctftools.crypto.number import btoi, egcd, itob, modinv


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
