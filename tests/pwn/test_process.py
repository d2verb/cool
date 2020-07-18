import pathlib
import platform
from os.path import join

from cool.pwn import process

BINPATH = join(pathlib.Path(__file__).parent.absolute(), "testbins")
BINNAME = {"Linux": "test_echo_x64.elf", "Darwin": "test_echo_x64.macho"}
OS = platform.system()


def test_process():
    p = process(join(BINPATH, BINNAME[OS]))

    assert p.recvuntil(b">> ") == b">> "

    p.sendline(b"hoge")
    assert p.recvuntil(b"\n", drop=True) == b"hoge"

    p.sendafter(b">> ", b"fuga\n")
    assert p.recvuntil(b"\n", drop=True) == b"fuga"

    p.sendlineafter(b">> ", b"piyo")
    assert p.recvuntil(b"\n", drop=True) == b"piyo"

    p.close()


def test_timeout():
    # passing the timeout parameter as a method argument
    p = process(join(BINPATH, BINNAME[OS]))
    timed_out = False
    try:
        p.recvuntil(b"meme", timeout=1)
    except TimeoutError:
        timed_out = True
    except Exception:
        pass
    finally:
        p.close()
    assert timed_out

    # passing the timeout parameter as a constructor argument
    p = process(join(BINPATH, BINNAME[OS]), timeout=1)
    timed_out = False
    try:
        p.recvuntil(b"meme")
    except TimeoutError:
        timed_out = True
    except Exception:
        pass
    finally:
        p.close()
    assert timed_out
