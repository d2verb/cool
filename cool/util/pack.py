def p16(number: int, endian: str = "little") -> bytes:
    return number.to_bytes(2, byteorder=endian)


def p32(number: int, endian: str = "little") -> bytes:
    return number.to_bytes(4, byteorder=endian)


def p64(number: int, endian: str = "little") -> bytes:
    return number.to_bytes(8, byteorder=endian)


def u16(data: bytes, endian: str = "little", signed: bool = False) -> int:
    return int.from_bytes(data, byteorder=endian, signed=signed)


def u32(data: bytes, endian: str = "little", signed: bool = False) -> int:
    return int.from_bytes(data, byteorder=endian, signed=signed)


def u64(data: bytes, endian: str = "little", signed: bool = False) -> int:
    return int.from_bytes(data, byteorder=endian, signed=signed)
