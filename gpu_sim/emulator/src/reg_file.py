from bitstring import Bits 

class Reg_File:
    def __init__(self, num_regs: int = 64, num_bits_per_reg: int = 32) -> None:
        self.arr: list[Bits] = [Bits(int=0, length=num_bits_per_reg) for i in range(num_regs)]
    
    def read(self, rd: Bits) -> Bits:
        return self.arr[rd.int]

    def write(self, rd: Bits, val: Bits) -> None:
        if(rd.int == 0):
            return
        self.arr[rd.int] = val

    @staticmethod
    def _get_local_thread_id_from(global_thread_id: int) -> int:
        return global_thread_id % 32
