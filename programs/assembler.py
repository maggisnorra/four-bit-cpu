INSTRUCTION_OPCODES = {
    "NOP": 0x0,
    "NOT": 0x1,
    "SHL": 0x2,
    "SHR": 0x3,
    "OUT": 0x4, # imm4
    "IN":  0x5, # imm4
    "LDI": 0x6, # imm4
    "ADI": 0x7, # imm4
    "JMP": 0x8, # addr
    "AND": 0x9, # addr
    "JC":  0xA, # addr
    "LDA": 0xB, # addr
    "STA": 0xC, # addr
    "OR":  0xD, # addr
    "JZ":  0xE, # addr
    "ADD": 0xF, # addr
}
IMMEDIATE_INSTRUCTIONS = ["OUT", "IN", "LDI", "ADI"]
ADDRESS_INSTRUCTIONS = ["JMP", "AND", "JC", "LDA", "STA", "OR", "JZ", "ADD"]

def parse_number(s: str) -> int | None:
    try:
        return int(s, 0)
    except ValueError:
        return None

def assembler(asm: str) -> str:
    
    # remove comments
    lines = asm.splitlines()
    without_comments = ""
    for line in lines:
        without_comments += " " + line.split("//")[0]
    
    # split into substrings
    substrings = without_comments.split()
    
    # validate
    for i, substring in enumerate(substrings):
        if substring in INSTRUCTION_OPCODES.keys():
            # instruction
            continue
        if parse_number(substring) is not None:
            # number
            continue
        if substring[:-1].replace("_", "").isalnum() and substring[-1] == ":":
            # label
            continue
        if i > 0 and substring.replace("_", "").isalnum() and substrings[i-1] in ADDRESS_INSTRUCTIONS:
            # label reference
            continue
        raise Exception(f"non-valid substring: {substring}")
    
    # locate/remove labels and expand addresses
    labels = {}
    ir = []
    address = 0x00
    last_was_address_instr = False
    last_was_immediate_instr = False
    for substring in substrings:
        if last_was_address_instr:
            val = parse_number(substring)
            if val is not None:
                if not 0 <= val <= 0xFF:
                    raise Exception(f"address to large or small {val}")
                ir += [(val >> 4) & 0xF]
                ir += [val & 0xF]
            elif substring.replace("_", "").isalnum():
                ir += [substring]
                ir += [""]
            else:
                raise Exception(f"invalid address or label: {substring}")
            address += 2
            last_was_address_instr = False
            continue
        if last_was_immediate_instr:
            val = parse_number(substring)
            if val is not None:
                if not 0 <= val <= 0xF:
                    raise Exception(f"immediate to large or small {val}")
                ir += [val & 0xF]
            else:
                raise Exception(f"invalid immediate: {substring}")
            address += 1
            last_was_immediate_instr = False
            continue
        if substring.endswith(":"):
            # label found
            if substring[:-1] in labels.keys():
                raise Exception(f"duplicate label: {substring[:-1]}")
            labels[substring[:-1]] = address
            continue
        if substring in INSTRUCTION_OPCODES.keys():
            ir += [substring]
            address += 1
            last_was_address_instr = substring in ADDRESS_INSTRUCTIONS
            last_was_immediate_instr = substring in IMMEDIATE_INSTRUCTIONS
            continue
        raise Exception(f"unexpected substring: {substring}")
    
    if last_was_address_instr:
        raise Exception("missing address operand")

    if last_was_immediate_instr:
        raise Exception("missing immediate operand")
    
    if address > 0x100:
        raise Exception("program does not fit in 256 nibble instruction memory")
        
    # replace label references
    for i, substring in enumerate(ir):
        if substring in labels.keys():
            ir[i] = (labels[substring] >> 4) & 0xF
            ir[i + 1] = labels[substring] & 0xF
    
    # replace with opcode and insert newline
    machine_code = ""
    for item in ir:
        if isinstance(item, str):
            machine_code += f"{INSTRUCTION_OPCODES[item]:X}\n"
        else:
            machine_code += f"{item:X}\n"
            
    return machine_code


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("asm_file")
    args = parser.parse_args()
    
    asm_path = Path(args.asm_file)

    with asm_path.open() as f:
        asm = f.read()

    machine_code = assembler(asm)

    output_dir = asm_path.parent / asm_path.stem
    output_dir.mkdir(exist_ok=True)

    with (output_dir / "instr_mem.hex").open("w") as f:
        f.write(machine_code)

    with (output_dir / "data_mem.hex").open("w") as f:
        f.write("0\n" * 256)
