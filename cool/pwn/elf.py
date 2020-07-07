import os
from typing import BinaryIO, Dict, Optional

from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.elf.sections import SymbolTableSection

from cool.util import u32


class ELF(ELFFile):
    path: str
    file: BinaryIO
    _got: Optional[Dict[str, int]]
    _plt: Optional[Dict[str, int]]
    _symbols: Optional[Dict[str, int]]

    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self.file = open(self.path, "rb")
        self._got = None
        self._plt = None
        self._symbols = None
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

    @property
    def plt(self) -> Dict[str, int]:
        if self._plt:
            return self._plt

        self._plt = {}

        got2plt = {}

        # make got_addr -> plt_addr mapping
        for plt_name in [".plt", ".plt.got", ".plt.sec"]:
            section = self.get_section_by_name(plt_name)

            if not section:
                continue

            mapping = self.__make_got_plt_mapping(
                code=section.data(),
                sh_addr=section.header.sh_addr,
                sh_size=section.header.sh_size,
            )
            got2plt.update(mapping)

        # make got_name -> plt_addr mapping
        for got_name, got_addr in self.got.items():
            if got_addr in got2plt:
                self._plt[got_name] = got2plt[got_addr]

        return self._plt

    def __make_got_plt_mapping(
        self, code: bytes, sh_addr: int, sh_size: int
    ) -> Dict[int, int]:
        machine = self.header.e_machine
        mapping = {}

        # TODO: implementation for other architectures
        if machine == "EM_X86_64":
            i = 0
            while i + 6 < sh_size:
                plt_va = sh_addr + i

                # jmp QWORD PTR [rip+imm]
                if code[i : i + 2] == b"\xff\x25":
                    imm = u32(code[i + 2 : i + 6])
                    rip = plt_va + 6

                    got_addr = rip + imm
                    mapping[got_addr] = plt_va
                    i += 6
                else:
                    i += 1
            return mapping
        else:
            raise NotImplementedError(
                f"making got-plt mapping for '{machine}' is not implemented now."
            )

    @property
    def symbols(self) -> Dict[str, int]:
        if self._symbols:
            return self._symbols

        self._symbols = {}

        for section in self.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue

            for symbol in section.iter_symbols():
                if symbol.name and symbol.entry.st_value:
                    self._symbols[symbol.name] = symbol.entry.st_value

        return self._symbols


def elf(path: str) -> ELF:
    return ELF(path)
