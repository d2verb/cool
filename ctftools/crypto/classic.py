import codecs


def rot13(s: str) -> str:
    return codecs.encode(s, "rot13")
