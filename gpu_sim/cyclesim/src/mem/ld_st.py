import enum
from typing import Dict, List, Optional
import logging
from bitstring import Bits


# from gpu_sim.cyclesim.test import ldst
# from gpu_sim.cyclesim.src.mem import dcache
from gpu_sim.cyclesim.src.mem.base import dMemResponse, dCacheRequest, LatchIF, ForwardingIF
from gpu_sim.cyclesim.latch_forward_stage import Instruction
from gpu_sim.cyclesim.custom_enums_multi import I_Op, S_Op


logger = logging.getLogger(__name__)


class Ldst_Fu:
    def __init__(self, mshr_size=4, ldst_q_size=4):
        self.ldst_q: list[pending_mem] = []
        self.ldst_q_size: int = ldst_q_size

        # self.dcache_if: Optional[LatchIF] = None
        # self.issue_if: Optional[LatchIF] = None
        # self.wb_if: Optional[LatchIF] = None
        # self.sched_if: Optional[ForwardingIF] = None

        self.wb_buffer = [] #completed dcache access buffer

        self.outstanding = False #Whether we have an outstanding dcache request

    def connect_interfaces(self, dcache_if: LatchIF, issue_if: LatchIF, wb_if: LatchIF, sched_if: ForwardingIF):
        self.dcache_if: LatchIF = dcache_if
        self.issue_if: LatchIF = issue_if
        self.wb_if: LatchIF = wb_if
        self.sched_if: ForwardingIF = sched_if
    
    def forward_miss(self, instr: Instruction):
        self.sched_if.push(instr)

    def tick(self):

        if len(self.ldst_q) + 1 < self.ldst_q_size:
            instr = self.issue_if.pop()
            if instr != None:
                self.ldst_q.append(instr)

        #apply backpressure if ldst_q full
        if len(self.ldst_q) == self.ldst_q_size:
            self.issue_if.forward_if.set_wait(True)
        else:
            self.issue_if.forward_if.set_wait(False)

        #send instr to wb if ready
        if self.wb_if.ready_for_push() and len(self.wb_buffer) > 0:
            self.wb_if.push(self.wb_buffer.pop(0).instr)

        #send req to cache if not waiting for response
        if self.outstanding == False and self.dcache_if.ready_for_push() and len(self.ldst_q) > 0:
            self.dcache_if.push(
                self.ldst_q[0].genReq()
            )
            self.outstanding = True

        #move mem_req to wb_buffer if finished
        if self.outstanding == False and self.ldst_q[0].readyWB():
            self.wb_buffer.append(self.ldst_q.pop(0))

        #handle dcache packet
        if self.dcache_if.forward_if.pop():
            if len(self.ldst_q) == 0:
                logger.warning(f"LSQ is length 0 and recieved a dcache response")

            payload: dMemResponse = self.dcache_if.forward_if.pop()

            mem_req = self.ldst_q[0]
            match payload.type:
                case 'MISS_ACCEPTED':
                    mem_req.parseMiss(payload)     
                    self.outstanding = False                   
                case 'HIT_STALL':
                    pass
                case 'MISS_COMPLETE':
                    mem_req.parseMshrHit(payload)
                case 'FLUSH_COMPLETE':
                    pass
                case 'HIT_COMPLETE':
                    mem_req.parseHit(payload)
                    self.outstanding = False
            

        


class pending_mem():
    def __init__(self, instr) -> None:
        self.instr: Instruction = instr
        self.finished_idx: List[int] = [0 for i in range(32)]
        self.write: bool
        self.mshr_idx: List[int] = [0 for i in range(32)]
        self.addrs = []

        match self.instr.opcode:
            case I_Op.LW.value:
                self.write = False
                self.size = "word"
            case I_Op.LH.value:
                self.write = False
                self.size = "half"
            case I_Op.LB.value:
                self.write = False
                self.size = "byte"
            
            case S_Op.SW.value:
                self.write = True
                self.size = "word"
            case S_Op.SH.value:
                self.write = True
                self.size = "half"
            case S_Op.SB.value:
                self.write = True
                self.size = "byte"
        
        for i in range(32):
            self.finished_idx[i] = 1-self.instr.predicate[i].int #iirc predicate=1'b1
            self.addrs[i] = self.instr.rs1.int + self.instr.imm.int if self.instr.predicate[i] else None
    
    def readyWB(self):
        return all(self.finished_idx)
    
    def genReq(self):
        for i in range(32):
            if self.finished_idx[i] == 0 and self.mshr_idx[i] == 0:
                return dCacheRequest(
                    addr_val=self.addrs[i],
                    rw_mode='write' if self.write else 'read',
                    size=self.size,
                    store_value=self.instr.rdat2[i].int
                )
        
        return None
    def parseHit(self, payload):
        for i in range(32):
            if self.addrs[i] == payload.address:
                self.finished_idx[i] = 1

                #set wdat if instr is a read
                if self.write == False:
                    self.instr.wdat[i] = Bits(payload.data, 32)

    
    def parseMshrHit(self, payload):
        if self.write:
            self.parseHit(payload)
        else:
            for i in range(32):
                if self.addrs[i] == payload.address and self.mshr_idx[i] == 1:
                    self.mshr_idx[i] = 0
    
    def parseMiss(self, payload: dMemResponse):
        for i in range(32):
            if self.addrs[i] == payload.address:
                self.mshr_idx[i] = 1

