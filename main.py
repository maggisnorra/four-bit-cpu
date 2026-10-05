class Nibble:
    def __init__(self, val=0):        
        self.value = val % 4
        
    def get(self):
        self.value
        
    def set(self, val):
        self.value = val % 4

class Memory:
    pass

class DataMemory(Memory):
    pass

class InstructionMemory(Memory):
    pass

class Cpu:
    def __init__(self):
        pass
    
    def nop():
        """nothing"""
        pass
    
    def not_opcode():
        """bitwise NOT accumulator"""
        pass
    
    def shl():
        """shift accumulator left"""
        pass
    
    def shr():
        """shift accumulator right |"""
        pass
    
    def out():
        """output accumulator with port as immediate"""
        pass
    
    def in_opcode():
        """load from input to accumulator with port as immediate"""
        pass

    def ldi():
        """load an immediate to accumulator"""
        pass

    def adi():
        """add immediate to accumulator"""
        pass

    def jmp():
        """unconditional jump"""
        pass

    def and_opcode():
        """bitwise AND with accumulator and memory"""
        pass

    def jc():
        """jump if carry flag is set"""
        pass

    def lda():
        """load to accumulator from memory"""
        pass

    def sta():
        """store accumulator to memory"""
        pass

    def or_opcode():
        """bitwise OR with accumulator and memory"""
        pass

    def jz():
        """jump if zero flag is set"""
        pass

    def add():
        """add to accumulator from memory"""
        pass
    
    def alu():
        pass

    def tick():
        pass

if __name__ == "__main__":
    pass
