from bitstring import Bits 
class Reg_File:
    def __init__(self, size=64) -> None:
        self.arr: list[int | float] = [0 for i in range(size)]
    
    def read(self, idx: int) -> int | float: #potential problem: if you read from a register initially (rdat=0), it wouldn't be a "Bits" type 
        return Bits(int=(self.arr[idx]), length=32)

    def write(self, idx: int, val: int | float) -> None:
        self.arr[idx] = Bits(int=val, length=32)
