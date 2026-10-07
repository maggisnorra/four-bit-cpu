from typing import Callable

from data_types import Nibble, Address

class Memory:
    
    memory_access_cycles: int
    
    def __init__(self, hex: str | list):
        self.data = [Nibble() for _ in range(2**8)]
        
        if isinstance(hex, str):
            hex = map(lambda x: int(f"0x{x}", 0), hex.split())
            
        for i, instruction in enumerate(hex):
            self.data[i] = Nibble(instruction)


class DataMemory(Memory):
    def read(self, addr: Address) -> Nibble:
        return self.data[addr.get()].copy()
    
    def write(self, addr: Address, value: Nibble) -> None:
        self.data[addr.get()] = value.copy()


class InstructionMemory(Memory):
    def read(self, addr: Address) -> Nibble:
        return self.data[addr.get()].copy()


class Cpu:
    
    data_mem: DataMemory
    instr_mem: InstructionMemory
    
    pc: Address
    accumulator: Nibble
    carry_flag: bool
    zero_flag: bool
    
    instruction: Nibble | None
    immediate: Nibble | None
    address: Address | None
    address_high: Nibble | None
    address_low: Nibble | None
    extra_cycles: int | None
    
    def __init__(self, data: DataMemory, program: InstructionMemory):
        self.data_mem = data
        self.instr_mem = program
        
        self.pc = Address()
        self.accumulator = Nibble()
        self.carry_flag = False
        self.zero_flag = False
        
        self.instruction = None
        self.immediate = None
        self.address = None
        self.address_high = None
        self.address_low = None
        self.extra_cycles = None
    
    def instr_nop(self) -> None:
        """nothing"""
        self.retire_instruction()
    
    def instr_not(self) -> None:
        """bitwise NOT accumulator"""
        self.accumulator = ~self.accumulator
        self.retire_instruction()
    
    def instr_shl(self) -> None:
        """shift accumulator left"""
        self.accumulator = self.accumulator << 1
        self.retire_instruction()
    
    def instr_shr(self) -> None:
        """shift accumulator right"""
        self.accumulator = self.accumulator >> 1
        self.retire_instruction()
    
    def instr_out(self) -> None:
        """output accumulator with port as immediate"""
        print(self.accumulator.get(), "to", self.immediate.get())
        self.retire_instruction()
    
    def instr_in(self) -> None:
        """load from input to accumulator with port as immediate"""
        self.accumulator = Nibble(int(input()))
        self.retire_instruction()

    def instr_ldi(self) -> None:
        """load an immediate to accumulator"""
        self.accumulator = self.immediate.copy()
        self.retire_instruction()

    def instr_adi(self) -> None:
        """add immediate to accumulator"""
        self.accumulator += self.immediate
        self.retire_instruction()
        
    def instr_immediate(self) -> None:
        if self.immediate is None:
            self.fetch_immediate()
        else:
            match self.instruction.get():
                case 0x4:
                    self.execute_after_cycles(4, self.instr_out)
                case 0x5:
                    self.execute_after_cycles(4, self.instr_in)
                case 0x6:
                    self.execute_after_cycles(4, self.instr_ldi)
                case 0x7:
                    self.execute_after_cycles(4, self.instr_adi)

    def instr_jmp(self) -> None:
        """unconditional jump"""
        self.pc = self.address.copy()
        self.retire_instruction()

    def instr_and(self) -> None:
        """bitwise AND with accumulator and memory"""
        self.accumulator &= self.load(self.address)
        self.retire_instruction()

    def instr_jc(self) -> None:
        """jump if carry flag is set"""
        if self.carry_flag:
            self.pc = self.address.copy()
        self.retire_instruction()

    def instr_lda(self) -> None:
        """load to accumulator from memory"""
        self.accumulator = self.load(self.address)
        self.retire_instruction()

    def instr_sta(self) -> None:
        """store accumulator to memory"""
        self.store(self.address, self.accumulator)
        self.retire_instruction()

    def instr_or(self) -> None:
        """bitwise OR with accumulator and memory"""
        self.accumulator |= self.load(self.address)
        self.retire_instruction()

    def instr_jz(self) -> None:
        """jump if zero flag is set"""
        if self.zero_flag:
            self.pc = self.address.copy()
        self.retire_instruction()

    def instr_add(self) -> None:
        """add to accumulator from memory"""
        self.accumulator += self.load(self.address)
        self.retire_instruction()
            
    def instr_address(self) -> None:
        if self.address is None:
            self.fetch_address()
        else:
            match self.instruction.get():
                case 0x8:
                    self.execute_after_cycles(4, self.instr_jmp)
                case 0x9:
                    self.execute_after_cycles(4, self.instr_and)
                case 0xA:
                    self.execute_after_cycles(4, self.instr_jc)
                case 0xB:
                    self.execute_after_cycles(4, self.instr_lda)
                case 0xC:
                    self.execute_after_cycles(4, self.instr_sta)
                case 0xD:
                    self.execute_after_cycles(4, self.instr_or)
                case 0xE:
                    self.execute_after_cycles(4, self.instr_jz)
                case 0xF:
                    self.execute_after_cycles(4, self.instr_add)
    
    def fetch_immediate(self) -> None:
        self.immediate = self.instr_mem.read(self.pc)
        self.pc.increment()
        
    def fetch_address(self) -> None:
        """state machine"""
        if self.address_high is None:
            self.address_high = self.instr_mem.read(self.pc)
        else:
            self.address_low = self.instr_mem.read(self.pc)
            self.address = Address(high=self.address_high.get(), low=self.address_low.get())
        self.pc.increment()
    
    def fetch_instruction(self) -> None:
        self.instruction = self.instr_mem.read(self.pc)
        self.pc.increment()
    
    def execute_after_cycles(self, cycles: int, func: Callable[[], None]):
        """state machine"""
        if self.extra_cycles is None:
            self.extra_cycles = cycles
        
        self.extra_cycles -= 1
        
        if self.extra_cycles <= 0:
            func()
        
    def retire_instruction(self) -> None:
        self.instruction = None
        self.immediate = None
        self.address = None
        self.address_high = None
        self.address_low = None
        self.extra_cycles = None
    
    def load(self, addr: Address) -> Nibble:
        return self.data_mem.read(addr)

    def store(self, addr: Address, value: Nibble) -> None:
        self.data_mem.write(addr, value)
                
    def tick(self):
        """one cycle pass"""
        if self.instruction is None:
            self.fetch_instruction()
        else:
            match self.instruction.get():
                case 0x0:
                    self.execute_after_cycles(4, self.instr_nop)
                case 0x1:
                    self.execute_after_cycles(4, self.instr_not)
                case 0x2:
                    self.execute_after_cycles(4, self.instr_shl)
                case 0x3:
                    self.execute_after_cycles(4, self.instr_shr)
                case i if 0x4 <= i <= 0x7:
                    self.instr_immediate()
                case i if 0x8 <= i <= 0xF:
                    self.instr_address()


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    args = parser.parse_args()
    
    program_directory = Path("../programs") / args.program
    
    data_hex_file = program_directory / "data_mem.hex"
    program_hex_file = program_directory / "instr_mem.hex"

    with data_hex_file.open() as f:
        data_hex = f.read()
        
    with program_hex_file.open() as f:
        program_hex = f.read()
    
    data = DataMemory(data_hex)
    program = InstructionMemory(program_hex)
    
    cpu = Cpu(data, program)
    
    cycle = 0
    while True:
        cpu.tick()
        cycle += 1
