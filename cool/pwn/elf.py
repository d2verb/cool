import os
from typing import BinaryIO, Dict
from functools import cached_property

from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.elf.sections import SymbolTableSection

from cool.util import u32


class ELF(ELFFile):
    """Class for accessing information in the ELF file.

    :param path: target ELF file path
    """

    path: str
    file: BinaryIO

    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self.file = open(self.path, "rb")
        super().__init__(self.file)

    @cached_property
    def got(self) -> Dict[str, int]:
        """Global offset table (GOT) entries.
        """
        got = {}
        for section in self.iter_sections():
            if not isinstance(section, RelocationSection):
                continue

            symtab = self.get_section(section.header.sh_link)

            for rel in section.iter_relocations():
                symbol = symtab.get_symbol(rel.entry.r_info_sym)
                got[symbol.name] = rel.entry.r_offset

        return got

    @cached_property
    def plt(self) -> Dict[str, int]:
        """Procedure linkage table (PLT) entries.
        """
        plt, got2plt = {}, {}
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
                plt[got_name] = got2plt[got_addr]

        return plt

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

    @cached_property
    def symbols(self) -> Dict[str, int]:
        """Symbols and their address.
        """
        symbols = {}
        for section in self.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue

            for symbol in section.iter_symbols():
                if symbol.name and symbol.entry.st_value:
                    symbols[symbol.name] = symbol.entry.st_value

        return symbols


def elf(path: str) -> ELF:
    """Open the ELF file and return its ELF class object.

    :param path: target ELF file path
    """
    return ELF(path)
