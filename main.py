class Nibble:
    def __init__(self, val=0):        
        self.value = val % 4
        
    def get(self):
        self.value
        
    def set(self, val):
        self.value = val % 4

class Address:
    def __init__(self, high=0, low=0):
        self.addr = ((high % 4) << 4) + low % 4
        
    def get(self):
        self.value
        
    def set(self, high, low):
        self.addr = ((high % 4) << 4) + low % 4

class Memory:
    def __init__(self):
        pass
    
    def memory_access_cycles():
        return 2

class DataMemory(Memory):
    def read(addr: Address):
        pass
    
    def write(addr: Address, value: Nibble):
        pass

class InstructionMemory(Memory):
    def read(addr: Address):
        pass

class Cpu:
    
    clock_cycle: int
    
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
    
    def __init__(self, data: DataMemory, program: InstructionMemory):
        self.data_mem = data
        self.instr_mem = program
        
        self.pc = 0
        self.accumulator = 0
        self.carry_flag = False
        self.zero_flag = False
        
        self.instruction = None
        self.immediate = None
        self.address = None
        self.address_high = None
        self.address_low = None
    
    def instr_nop(self) -> None:
        """nothing"""
        None
    
    def instr_not(self) -> None:
        """bitwise NOT accumulator"""
        self.accumulator = ~self.accumulator
    
    def instr_shl(self) -> None:
        """shift accumulator left"""
        self.accumulator = self.accumulator << 1
    
    def instr_shr(self) -> None:
        """shift accumulator right"""
        self.accumulator = self.accumulator >> 1
    
    def instr_out(self) -> None:
        """output accumulator with port as immediate"""
        pass
    
    def instr_in(self) -> None:
        """load from input to accumulator with port as immediate"""
        pass

    def instr_ldi(self) -> None:
        """load an immediate to accumulator"""
        self.accumulator = self.fetch_immediate()

    def instr_adi(self) -> None:
        """add immediate to accumulator"""
        self.accumulator += self.fetch_immediate()
        
    def instr_immediate(self) -> None:
        if self.immediate:
            match self.instruction:
                case 0x4:
                    self.instr_out()
                case 0x5:
                    self.instr_in()
                case 0x6:
                    self.instr_ldi()
                case 0x7:
                    self.instr_adi()
        else:
            self.fetch_immediate()

    def instr_jmp(self) -> None:
        """unconditional jump"""
        self.pc = self.fetch_address()

    def instr_and(self) -> None:
        """bitwise AND with accumulator and memory"""
        self.accumulator &= self.load(self.fetch_address())

    def instr_jc(self) -> None:
        """jump if carry flag is set"""
        addr = self.fetch_address()
        if self.carry_flag:
            self.pc = addr

    def instr_lda(self) -> None:
        """load to accumulator from memory"""
        self.accumulator = self.load(self.fetch_address())

    def instr_sta(self) -> None:
        """store accumulator to memory"""
        self.store(self.fetch_address(), self.accumulator)

    def instr_or(self) -> None:
        """bitwise OR with accumulator and memory"""
        self.accumulator |= self.load(self.fetch_address())

    def instr_jz(self) -> None:
        """jump if zero flag is set"""
        if self.zero_flag:
            self.pc = self.address

    def instr_add(self) -> None:
        """add to accumulator from memory"""
        self.accumulator += self.load(self.address)
            
    def instr_address(self) -> None:
        if self.address:
            match self.instruction:
                case 0x8:
                    self.instr_jmp()
                case 0x9:
                    self.instr_and()
                case 0xA:
                    self.instr_jc()
                case 0xB:
                    self.instr_lda()
                case 0xC:
                    self.instr_sta()
                case 0xD:
                    self.instr_or()
                case 0xE:
                    self.instr_jz()
                case 0xF:
                    self.instr_add()
        else:
            self.fetch_address()
    
    def fetch_immediate(self) -> Nibble:
        self.pc += 1
        self.immediate = self.instr_mem.read(self.pc)
        
    def fetch_address(self) -> Address:
        self.pc += 1
        high_addr = self.instr_mem.read(self.pc)
        self.pc += 1
        low_addr = self.instr_mem.read(self.pc)
        self.address = Address(high=high_addr, low=low_addr)
    
    def fetch_instruction(self) -> Nibble:
        self.pc += 1
        return self.instr_mem.read(self.pc)
    
    def load(self, addr: Address):
        self.data_mem.read(addr)

    def store(self, addr: Address, value: Nibble):
        self.data_mem.write(addr, value)
                
    def tick(self):
        """one cycle pass"""
        
        if not self.instruction:
            self.instruction = self.fetch_instruction()
        else:
            match self.fetch_instruction():
                case 0x0:
                    self.instr_nop()
                case 0x1:
                    self.instr_not()
                case 0x2:
                    self.instr_shl()
                case 0x3:
                    self.instr_shr()
                case i if 0x4 <= i <= 0x7:
                    self.instr_immediate()
                case i if 0x8 <= i <= 0xF:
                    self.instr_address()

if __name__ == "__main__":
    pass
