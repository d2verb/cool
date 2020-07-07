def p16(d: int, endian: str = "little") -> bytes:
    return d.to_bytes(2, byteorder=endian)


def p32(d: int, endian: str = "little") -> bytes:
    return d.to_bytes(4, byteorder=endian)


def p64(d: int, endian: str = "little") -> bytes:
    return d.to_bytes(8, byteorder=endian)


def u16(d: bytes, endian: str = "little", signed: bool = False) -> int:
    return int.from_bytes(d, byteorder=endian, signed=signed)


def u32(d: bytes, endian: str = "little", signed: bool = False) -> int:
    return int.from_bytes(d, byteorder=endian, signed=signed)


def u64(d: bytes, endian: str = "little", signed: bool = False) -> int:
    return int.from_bytes(d, byteorder=endian, signed=signed)
