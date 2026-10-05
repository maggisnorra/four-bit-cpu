# 4-bit CPU

By Maggi

Little or big endian?

one register/accumulator.

address is a byte (8 bits)

immediate is 4 bits

## Instruction Set (ISA)

| Opcode | Hex | Instuction | Argument | Description |
| ------ | --- | ---------- | -------- | ----------- |
|   0000 | 0x0 | NOP        |     none | nothing |
|   0001 | 0x1 | NOT        |     none | bitwise NOT accumulator |
|   0010 | 0x2 | SHL        |     none | shift accumulator left |
|   0011 | 0x3 | SHR        |     none | shift accumulator right |
|   0100 | 0x4 | OUT        |     imm4 | output accumulator with port as immediate |
|   0101 | 0x5 | IN         |     imm4 | load from input to accumulator with port as immediate |
|   0110 | 0x6 | LDI        |     imm4 | load an immediate to accumulator |
|   0111 | 0x7 | ADI        |     imm4 | add immediate to accumulator |
|   1000 | 0x8 | JMP        |     addr | unconditional jump |
|   1001 | 0x9 | AND        |     addr | bitwise AND with accumulator and memory |
|   1010 | 0xA | JC         |     addr | jump if carry flag is set |
|   1011 | 0xB | LDA        |     addr | load to accumulator from memory |
|   1100 | 0xC | STA        |     addr | store accumulator to memory |
|   1101 | 0xD | OR         |     addr | bitwise OR with accumulator and memory |
|   1110 | 0xE | JZ         |     addr | jump if zero flag is set |
|   1111 | 0xF | ADD        |     addr | add to accumulator from memory |

Opcode binary is:
- op3 = followed by an address
- op2 = followed by an immediate if not an address
- op1 = second LSB
- op0 = LSB

And:
- xx01 is bitwise (except for immediate)
- x000 is only move PC
- 1x10 is conditional branch
- x111 is add
- 010x is input/output
