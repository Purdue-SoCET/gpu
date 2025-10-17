class Reg_File:
    def __init__(self, size) -> None:
        self.arr: list[int | float] = [0 for i in range(size)]
    
    def read(self, idx: int) -> int | float:
        return self.arr[idx]

    def write(self, idx: int, val: int | float) -> None:
        self.arr[idx] = val
