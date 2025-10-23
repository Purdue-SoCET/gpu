#write into memsim.hex as hash table
import atexit

class Mem: 
    def __init__(self) -> None:
        self.memory = {}
        atexit.register(self.dump_on_exit)

    def read(self, addr: int) -> int:
        return self.memory.get(addr, 0)

    def write(self, addr: int, data: int) -> None:
        self.memory[addr] = data

    def dump_on_exit(self) -> None:
        try:
            self.dump("memsim.hex")
        except Exception:
            print("oopsie")
            pass
    
    # CAN CHANGE THIS SHIT LATER IF WE WANT TO PRINT OUT MORE INFO
    def dump(self, path: str = "memsim.hex") -> None:
        items = ((a, v) for a, v in self.memory.items() if v != 0)
        with open(path, "w", encoding="utf-8") as f:
            for addr, val in sorted(items, key=lambda x: x[0]):
                f.write(f"{addr:#x} {val:#x}\n")
    #dump into memsim.hex
        #copy meminit.hex into memsim