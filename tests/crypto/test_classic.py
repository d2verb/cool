from cool.crypto.classic import rot13, xorcipher


def test_rot13():
    # encryption
    assert rot13("Hello, World!") == "Uryyb, Jbeyq!"
    assert rot13("こんにちは, World!") == "こんにちは, Jbeyq!"

    # decryption
    assert rot13("Uryyb, Jbeyq!") == "Hello, World!"
    assert rot13("こんにちは, Jbeyq!") == "こんにちは, World!"


def test_xorcipher():
    key = b"\x00\x01\x02"
    plt = b"Hello, World!"
    enc = b"Hdnln. Vmrmf!"

    assert xorcipher(plt, key) == enc
    assert xorcipher(enc, key) == plt
