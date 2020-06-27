from typing import Optional, Tuple

from Crypto.PublicKey import RSA


def export_key(n: int, e: int, d: Optional[int] = None) -> bytes:
    if d is not None:
        key = RSA.construct((n, e, d))
    else:
        key = RSA.construct((n, e))
    return key.exportKey()


def import_key(
    content: str, passphrase: Optional[str] = None
) -> Tuple[int, int, Optional[int]]:
    key = RSA.import_key(content, passphrase)

    if key.has_private():
        return key.n, key.e, key.d
    else:
        return key.n, key.e, None
