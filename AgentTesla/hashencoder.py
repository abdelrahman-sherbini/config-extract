def sub_4010C6(a1):
    i = 0

    for v3 in a1:
        print(ord(v3),v3)
        i = ((ord(v3) | 0x21) ^ i)
        print(hex(i))
        i = ((i << 11) | (i >> (32 - 11))) & 0xFFFFFFFF
        print(hex(i))

    return i

input_str = "LdrGetDllHandle"
result = sub_4010C6(input_str)
print("Result: 0x{:X}".format(result))

