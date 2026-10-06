class Nibble:
    def __init__(self, val=0):        
        self.value = val & 0xF
        
    def get(self):
        return self.value
        
    def set(self, val):
        self.value = val & 0xF
        
    def copy(self):
        return Nibble(self.value)
    
    def __add__(self, val):
        return Nibble(self.value + val.get())
    
    def __invert__(self):
        return Nibble(~self.value)

    def __lshift__(self, val: int):
        return Nibble(self.value << val)

    def __rshift__(self, val: int):
        return Nibble(self.value >> val)

    def __and__(self, val):
        return Nibble(self.value & val.get())

    def __or__(self, val):
        return Nibble(self.value | val.get())


class Address:
    def __init__(self, high=0, low=0):
        self.addr = ((high & 0xF) << 4) + (low & 0xF)
        
    def get(self):
        return self.addr
        
    def set(self, high, low):
        self.addr = ((high & 0xF) << 4) + (low & 0xF)
        
    def increment(self):
        self.addr = (self.addr + 1) & 0xFF
    
    def copy(self):
        return Address(
            high=(self.addr >> 4) & 0xF,
            low=self.addr & 0xF
        )
        