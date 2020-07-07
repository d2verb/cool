import pathlib
from os.path import join

import pytest

from cool.pwn import elf

BINPATH = join(pathlib.Path(__file__).parent.absolute(), "testbins")


@pytest.mark.parametrize(
    ("filename", "gots"),
    [
        (
            "test_x64.elf",
            {
                "puts": 0x0601018,
                "__libc_start_main": 0x600FF0,
                "__gmon_start__": 0x600FF8,
            },
        ),
        (
            "test_x32.elf",
            {
                "puts": 0x804A00C,
                "__libc_start_main": 0x804A010,
                "__gmon_start__": 0x8049FFC,
            },
        ),
    ],
)
def test_got(filename, gots):
    filepath = join(BINPATH, filename)
    e = elf(filepath)

    assert len(e.got) == len(gots)
    for got_name, got_addr in gots.items():
        assert e.got[got_name] == got_addr


@pytest.mark.parametrize(
    ("filename", "plts"), [("test_x64.elf", {"puts": 0x4003F0})],
)
def test_plt(filename, plts):
    filepath = join(BINPATH, filename)
    e = elf(filepath)

    assert len(e.plt) == len(plts)
    for plt_name, plt_addr in plts.items():
        assert e.plt[plt_name] == plt_addr
