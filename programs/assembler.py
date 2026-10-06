INSTRUCTION_OPCODES = {
    "NOP": 0x0,
    "NOT": 0x1,
    "SHL": 0x1,
    "SHR": 0x1,
    "OUT": 0x1, # imm4
    "IN":  0x1, # imm4
    "LDI": 0x1, # imm4
    "ADI": 0x1, # imm4
    "JMP": 0x1, # addr
    "AND": 0x1, # addr
    "JC":  0x1, # addr
    "LDA": 0x1, # addr
    "STA": 0x1, # addr
    "OR":  0x1, # addr
    "JZ":  0x1, # addr
    "ADD": 0x1, # addr
}
IMMEDIATE_INSTRUCTIONS = ["OUT", "IN", "LDI", "ADI"]
ADDRESS_INSTRUCTIONS = ["JMP", "AND", "JC", "LDA", "STA", "OR", "JZ", "ADD"]


def first_pass(asm: str) -> list:
    pass

def second_pass(ir: list) -> str:
    pass



f = open("D:\\myfiles\welcome.txt")
print(f.read()) 

with open("demofile.txt") as f:
    print(f.read()) 

if __name__ is "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.parse_args()
