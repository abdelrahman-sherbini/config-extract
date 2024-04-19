import struct
import io
from zlib import crc32
from pwn import u64, p32


file= open("cleaned_dance", "rb")
file.seek(0x78a0)
crc_table = {}
table_88a0 = {}

#Rainbow Table for crc32(rip)
for i in range(0xfff+1):
        crc_table[crc32(p32(i))] = i
        #>>> p32(5)
        # b'\x05\x00\x00\x00' to bytes



while 1:


    # "<" indicates little-endian byte order. This means the least significant byte is stored first in memory.
    # I represents an unsigned integer of 4 bytes.
    # B represents an unsigned char of 1 byte.
    # 19B represents 19 unsigned chars (each of 1 byte)
    # intotal 24 where each part is 24 bytes &byte_88A0[24 * some_index + 5]
    code =struct.unpack("<IB19B",file.read(24))
    # print(code)
    crc = code[0]
    size = code[1]
    insn = bytes(code[2:])

    if crc == 0 and size ==0:
        break

    table_88a0[crc_table[crc]] = insn[:size]

elffile=open("out.elf","rb").read() #from cyberchef
elf_fp = io.BytesIO(elffile)
for addr,insns in table_88a0.items():
    elf_fp.seek(0x1000+addr)
    elf_fp.write(insns)
open("out2.elf","wb").write(elf_fp.getvalue())