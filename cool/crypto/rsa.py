from typing import Optional, Tuple

from Crypto.PublicKey import RSA

from cool.crypto.number import egcd
from gmpy2 import iroot


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


def low_public_exponent_attack(c: int, e: int) -> Optional[int]:
    m, result = iroot(c, e)
    return m if result else None


def common_modulus_attack(c1: int, e1: int, c2: int, e2: int, n: int) -> int:
    g, x, y = egcd(e1, e2)
    c1 = pow(c1, x, n)
    c2 = pow(c2, y, n)
    return (c1 * c2) % n
