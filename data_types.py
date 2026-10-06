class Nibble:
    def __init__(self, val=0):        
        self.value = val & 0xF
        
    def get(self):
        return self.value
        
    def set(self, val):
        self.value = val & 0xF
    
    def __add__(self, val: Nibble):
        return Nibble(self.value + val.get())


class Address:
    def __init__(self, high=0, low=0):
        self.addr = ((high & 0xF) << 4) + low & 0xF
        
    def get(self):
        return self.addr
        
    def set(self, high, low):
        self.addr = ((high & 0xF) << 4) + low & 0xF
        
    def increment(self):
        self.addr = (self.addr + 1) & 0xF
        