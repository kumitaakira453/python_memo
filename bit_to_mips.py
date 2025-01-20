## 2bit or 16bit => MIPS
def decode_mips_instruction(bitcode):
    """MIPS命令をデコード"""
    opcode = int(bitcode[:6], 2)

    if opcode == 0:
        # R形式
        return decode_r_format(bitcode)
    elif opcode in {2, 3}:
        # J形式
        return decode_j_format(bitcode)
    else:
        # I形式
        return decode_i_format(bitcode)


def decode_r_format(bitcode):
    """R形式デコード"""
    rs = int(bitcode[6:11], 2)
    rt = int(bitcode[11:16], 2)
    rd = int(bitcode[16:21], 2)
    shamt = int(bitcode[21:26], 2)
    funct = int(bitcode[26:], 2)

    funct_map = {
        32: "add",
        33: "addu",
        34: "sub",
        35: "subu",
        36: "and",
        37: "or",
        38: "xor",
        39: "nor",
        42: "slt",
        43: "sltu",
        0: "sll",
        2: "srl",
        3: "sra",
        4: "sllv",
        6: "srlv",
        8: "jr",
    }

    instruction = funct_map.get(funct, "unknown")
    if instruction in {"sll", "srl", "sra"}:
        return f"{instruction} ${rd}, ${rt}, {shamt}"
    elif instruction == "jr":
        return f"{instruction} ${rs}"
    elif instruction in {"sllv", "srlv"}:
        return f"{instruction} ${rd}, ${rt}, ${rs}"
    else:
        return f"{instruction} ${rd}, ${rs}, ${rt}"


def decode_i_format(bitcode):
    """I形式デコード"""
    opcode = int(bitcode[:6], 2)
    rs = int(bitcode[6:11], 2)
    rt = int(bitcode[11:16], 2)
    immediate = int(bitcode[16:], 2)

    opcode_map = {
        8: "addi",
        9: "addiu",
        12: "andi",
        13: "ori",
        14: "xori",
        15: "lui",
        35: "lw",
        43: "sw",
        10: "slti",
        11: "sltiu",
        4: "beq",
        5: "bne",
    }

    instruction = opcode_map.get(opcode, "unknown")
    if instruction in {"beq", "bne"}:
        return f"{instruction} ${rs}, ${rt}, {immediate}"
    elif instruction == "lui":
        return f"{instruction} ${rt}, {immediate}"
    else:
        return f"{instruction} ${rt}, ${rs}, {immediate}"


def decode_j_format(bitcode):
    """J形式デコード"""
    opcode = int(bitcode[:6], 2)
    address = int(bitcode[6:], 2)

    opcode_map = {2: "j", 3: "jal"}

    instruction = opcode_map.get(opcode, "unknown")
    return f"{instruction} {address}"


def decode_mips_instruction_with_hex(input_code):
    """
    MIPS命令をデコード (16進数入力対応)

    :param input_code: ビットコードまたは16進数の文字列
    :return: デコードされたMIPS命令
    """
    # 入力が16進数の場合、2進数に変換
    if input_code.startswith("0x") or input_code.startswith("0X"):
        bitcode = bin(int(input_code, 16))[2:].zfill(32)  # 32ビットを確保
    else:
        bitcode = input_code  # ビットコードのまま使用

    return decode_mips_instruction(bitcode)


# テスト用コード
test_inputs = [
    "00000010001100100100000000100000",  # 2進数: add $t0, $t1, $t2
    "0x02324020",  # 16進数: add $t0, $t1, $t2
    "0x2129000f",  # 16進数: addi $t1, $t1, 15
    "00001000000000000000000000001111",  # 2進数: j 15
    "0x0c00000f",  # 16進数: jal 15
]

# for input_code in test_inputs:
#     print(decode_mips_instruction_with_hex(input_code))

# print(decode_mips_instruction_with_hex())
BITS = "00000010001100100100000000100000"
print(decode_mips_instruction_with_hex(BITS))
