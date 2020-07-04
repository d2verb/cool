import os
from typing import BinaryIO, Dict, Optional

from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection


class ELF(ELFFile):
    path: str
    file: BinaryIO
    _got: Optional[Dict[str, int]]

    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self.file = open(self.path, "rb")
        self._got = None
        super().__init__(self.file)

    @property
    def got(self) -> Dict[str, int]:
        if self._got:
            return self._got

        self._got = {}

        for section in self.iter_sections():
            if not isinstance(section, RelocationSection):
                continue

            symtab = self.get_section(section.header.sh_link)

            for rel in section.iter_relocations():
                symbol = symtab.get_symbol(rel.entry.r_info_sym)
                self._got[symbol.name] = rel.entry.r_offset

        return self._got


def elf(path: str) -> ELF:
    return ELF(path)
