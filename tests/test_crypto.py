from ctftools.crypto.classic import rot13


def test_rot13():
    # encryption
    assert rot13("Hello, World!") == "Uryyb, Jbeyq!"
    assert rot13("こんにちは, World!") == "こんにちは, Jbeyq!"

    # decryption
    assert rot13("Uryyb, Jbeyq!") == "Hello, World!"
    assert rot13("こんにちは, Jbeyq!") == "こんにちは, World!"
