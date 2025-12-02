from typing import NamedTuple
from bitstring import Bits
from latch_forward_stage import LatchIF, ForwardingIF
from typing import Optional

class Ldst_Dcache_Payload(NamedTuple):
    addr: Bits
    write: bool # 1 for a write, 0 for a read
    pc: int

class Dcache_Ldst_Payload(NamedTuple):
    data: Optional[list[Bits]]
    addr: Bits
    pc: int
    hit: bool
    miss: bool

