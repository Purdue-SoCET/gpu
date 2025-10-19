from bitstring import Bits 
class Reg_File:
    def __init__(self, size=64) -> None:
        self.arr: list[Bits] = [Bits(int=0, length=32) for i in range(size)]
    
    def read(self, idx: int) -> Bits:
        return self.arr[idx]

    def write(self, idx: int, val: int | float) -> None:
        self.arr[idx] = Bits(int=val, length=32)
