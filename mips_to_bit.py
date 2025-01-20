register_map = {
    "zero": 0,
    "at": 1,
    "v0": 2,
    "v1": 3,
    "a0": 4,
    "a1": 5,
    "a2": 6,
    "a3": 7,
    "t0": 8,
    "t1": 9,
    "t2": 10,
    "t3": 11,
    "t4": 12,
    "t5": 13,
    "t6": 14,
    "t7": 15,
    "s0": 16,
    "s1": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "t8": 24,
    "t9": 25,
    "k0": 26,
    "k1": 27,
    "gp": 28,
    "sp": 29,
    "fp": 30,
    "ra": 31,
}


def encode_r_format(parts, instruction):
    funct_map = {
        "add": 32,
        "sub": 34,
        "addu": 33,
        "subu": 35,
        "and": 36,
        "or": 37,
        "nor": 39,
        "xor": 38,
        "sll": 0,
        "srl": 2,
        "sra": 3,
        "sllv": 4,
        "srlv": 6,
        "slt": 42,
        "sltu": 43,
        "jr": 8,
    }
    rd = register_map[parts[1].strip(",")[1:]]
    rs = register_map[parts[2].strip(",")[1:]]
    rt = (
        register_map[parts[3].strip(",")[1:]]
        if instruction not in {"sll", "srl", "sra"}
        else 0
    )
    shamt = int(parts[3]) if instruction in {"sll", "srl", "sra"} else 0
    funct = funct_map[instruction]
    binary = f"{0:06b}{rs:05b}{rt:05b}{rd:05b}{shamt:05b}{funct:06b}"
    hex_value = f"{int(binary, 2):08X}"
    return binary, hex_value


def encode_i_format(parts, instruction):
    opcode_map = {
        "addi": 8,
        "dddiu": 9,
        "andi": 12,
        "ori": 13,
        "xori": 14,
        "lw": 35,
        "sw": 43,
        "lui": 15,
        "slti": 10,
        "sltiu": 11,
        "beq": 4,
        "bne": 5,
    }
    opcode = opcode_map[instruction]
    rs = register_map[parts[2].strip(",")[1:]]
    rt = register_map[parts[1].strip(",")[1:]]
    immediate = int(parts[3])
    binary = f"{opcode:06b}{rs:05b}{rt:05b}{immediate:016b}"
    hex_value = f"{int(binary, 2):08X}"
    return binary, hex_value


def encode_j_format(parts, instruction):
    opcode_map = {"j": 2, "jal": 3}
    opcode = opcode_map[instruction]
    address = int(parts[1])
    binary = f"{opcode:06b}{address:026b}"
    hex_value = f"{int(binary, 2):08X}"
    return binary, hex_value


def encode_mips_instruction(asm):
    parts = asm.split()
    instruction = parts[0]
    if instruction in {
        "add",
        "sub",
        "addu",
        "subu",
        "and",
        "or",
        "nor",
        "xor",
        "sll",
        "srl",
        "sra",
        "sllv",
        "srlv",
        "slt",
        "sltu",
        "jr",
    }:
        return encode_r_format(parts, instruction)
    elif instruction in {
        "addi",
        "dddiu",
        "andi",
        "ori",
        "xori",
        "lw",
        "sw",
        "lui",
        "slti",
        "sltiu",
        "beq",
        "bne",
    }:
        return encode_i_format(parts, instruction)
    elif instruction in {"j", "jal"}:
        return encode_j_format(parts, instruction)
    else:
        return "unknown", "unknown"


asm_instructions = [
    "add $t0, $t1, $t2",  # R形式
    "addi $t2, $t1, 15",  # I形式
    "j 15",  # J形式
    "and $t0, $t1, $t2",  # R形式
    "ori $s2, $t1, 21",  # I形式
]

# for asm in asm_instructions:
#     binary, hex_value = encode_mips_instruction(asm)
#     print(f"ASM: {asm}\n２進数: {binary}\n16進数: {hex_value}\n")

# ASM = "add $t0, $t1, $t2"
ASM = "beq $t7, $t8, 20"
# ASM = "add $t0, $t1, $t2"
binary, hex_value = encode_mips_instruction(ASM)
print(f"ASM: {ASM}\n２進数: {binary}\n16進数: {hex_value}\n")
