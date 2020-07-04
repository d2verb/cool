from ctftools.util.pack import p16, p32, p64, u16, u32, u64


def test_p16():
    assert p16(0x4142, endian="little") == b"\x42\x41"
    assert p16(0x4142, endian="big") == b"\x41\x42"


def test_p32():
    assert p32(0x41424344, endian="little") == b"\x44\x43\x42\x41"
    assert p32(0x41424344, endian="big") == b"\x41\x42\x43\x44"


def test_p64():
    assert (
        p64(0x4142434445464748, endian="little") == b"\x48\x47\x46\x45\x44\x43\x42\x41"
    )
    assert p64(0x4142434445464748, endian="big") == b"\x41\x42\x43\x44\x45\x46\x47\x48"


def test_u16():
    assert u16(b"\x42\x41", endian="little") == 0x4142
    assert u16(b"\x41\x42", endian="big") == 0x4142


def test_u32():
    assert u32(b"\x44\x43\x42\x41", endian="little") == 0x41424344
    assert u32(b"\x41\x42\x43\x44", endian="big") == 0x41424344


def test_u64():
    assert (
        u64(b"\x48\x47\x46\x45\x44\x43\x42\x41", endian="little") == 0x4142434445464748
    )
    assert u64(b"\x41\x42\x43\x44\x45\x46\x47\x48", endian="big") == 0x4142434445464748
