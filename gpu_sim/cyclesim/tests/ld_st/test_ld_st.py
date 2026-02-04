from logging import handlers
from re import A
import unittest
import logging
import sys

# from gpu_sim.cyclesim.src.mem import dcache
from gpu_sim.cyclesim.src.mem.base import ForwardingIF, LatchIF, dCacheRequest, dMemResponse
from gpu_sim.cyclesim.src.mem.ld_st import Ldst_Fu
from gpu_sim.cyclesim.latch_forward_stage import Instruction, LatchIF, ForwardingIF
from bitstring import Bits

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

class TestLoadStoreUnit(unittest.TestCase):
    def genLoad(self,
                pc: Bits,
                rd=Bits(int=0, length=32),
                rdat1 = [Bits(int=0, length=32) for i in range(32)],
                rdat2 =  [Bits(int=0, length=32) for i in range(32)],
                wdat = [None for i in range(32)],
                pred = [Bits(bin='0b1', length=1) for i in range(32)]
            ) -> Instruction:
        instr = Instruction(pc=pc,
                            intended_FSU="ldst",
                            warp_id=0,
                            warp_group_id=0,
                            rs1=Bits(int=0,length=32),
                            rs2=Bits(int=0,length=32),
                            imm=Bits(int=0,length=32),
                            rd=rd,
                            wdat=wdat,
                            opcode=Bits(bin='0b0100000'),
                            rdat1 = rdat1,
                            rdat2 = rdat2,
                            predicate=pred
                            )
        # instr.pc = pc
        # instr.intended_FU = "ldst_fu"
        # instr.warp_id = 0
        # instr.warp_group_id = 0

        # instr.rs1 = 0
        # instr.rs2 = 0
        # instr.rd = rd
        # instr.opcode = Bits(bin="0b010000", length=4)

        # instr.rdat1 = rdat1
        # instr.rdat2 = rdat2
        # instr.wdat = wdat
        return instr
    
    def genStore(self, pc: int, rd=0, rdat1 = [Bits(int=0, length=32) for i in range(32)], rdat2 =  [Bits(int=0, length=32) for i in range(32)]) -> Instruction:
        instr = Instruction(pc=pc, intended_FU="ldst", warp_id=0, warp_group_id=0, rs1=0, rs2=0, rd=rd, opcode=Bits(bin='0b0110'))
        instr.pc = pc
        instr.intended_FU = "ldst_fu"
        instr.warp_id = 0
        instr.warp_group_id = 0

        instr.rs1 = 0
        instr.rs2 = 0
        instr.rd = rd
        instr.opcode = Bits(bin="0b0100", length=4)

        instr.rdat1 = rdat1
        instr.rdat2 = rdat2

        return instr
    
    def genHit(self, hex_data:str):
        dcache_req: dCacheRequest = self.dcache_if.pop()
        logging.info(f"Servicing hit for addr: {dcache_req.addr_val}")
        assert type(dcache_req) == dCacheRequest
        self.dcache_fwd.push(
            # dMemResponse(
            #     data=[Bits(hex=hex_data, length=32) for i in range(32)],
            #     pc=dcache_req.pc,
            #     hit=True,
            #     miss=False,
            #     addr=dcache_req.addr
            # )
            # dMemResponse(
            #             type = 'MISS_COMPLETE',
            #             uuid = uuid,
            #             req = req,
            #             address = req.addr_val,
            #             replay = True
            # )
            dMemResponse(
                type = 'HIT_COMPLETE',
                hit = True,
                req = dcache_req,
                address = dcache_req.addr_val,
                data = int(hex_data, 16)
            )
        )

    def mshrHit(self, mshr_data: tuple[int, Bits], hex_data:str):
        pc = mshr_data[0]
        addr = mshr_data[1]
        logging.info(f"Servicing MSHR hit for addr: {addr} for pc {pc}")

        self.dcache_fwd.push(
            Dcache_Ldst_Payload(
                data=[Bits(hex=hex_data, length=32) for i in range(32)],
                pc=pc,
                hit=True,
                miss=False,
                addr=addr
            )
        )

    def intToHex(self, num) -> str:
        return Bits(auto=num, length=32).hex()
    
    def genMiss(self) -> tuple[int, Bits]:
        dcache_req: Ldst_Dcache_Payload = self.dcache_if.pop()
        logging.info(f"Servicing miss for addr: {dcache_req.addr} for pc {dcache_req.pc}")

        if type(dcache_req) != Ldst_Dcache_Payload:
            logger.warning("Err in genMiss")
            logger.warning(f" {type(dcache_req)}")
            logger.warning(f" {dcache_req}")
            logger.warning(f" {self.dcache_if.valid}")

        assert type(dcache_req) == Ldst_Dcache_Payload
        self.dcache_fwd.push(
            Dcache_Ldst_Payload(
                data=None,
                pc=dcache_req.pc,
                hit=False,
                miss=True,
                addr=dcache_req.addr
            )
        )
        return (dcache_req.pc, dcache_req.addr)
        


    @classmethod
    def setUp(cls) -> None:
        cls.ldst_fu = Ldst_Fu()

        cls.dcache_if = LatchIF()
        cls.dcache_fwd = ForwardingIF()
        cls.dcache_if.forward_if = cls.dcache_fwd

        cls.issue_if = LatchIF()
        cls.issue_if_fwd = ForwardingIF()
        cls.issue_if.forward_if = cls.issue_if_fwd

        cls.wb_if = LatchIF()

        cls.sched_if = ForwardingIF()
        
        cls.ldst_fu.connect_interfaces(cls.dcache_if, cls.issue_if, cls.wb_if, cls.sched_if)
        cls.dcache_fwd.push(None)

    @unittest.skip("Skipping while singleLoadMiss isn't working")
    def test_singleLoadHit(self):
        instr = self.genLoad(pc=0, rd=0, rdat1 = [Bits(int=i, length=32) for i in range(0, 0x400, 32)])
        self.issue_if.push(instr)
        self.ldst_fu.tick()

        while not self.wb_if.valid:
            if self.dcache_if.valid:
                self.genHit('0xAA')
            else:
                self.dcache_fwd.push(None)
            self.ldst_fu.tick()
        self.dcache_if.valid = False

        instr: Instruction = self.wb_if.pop()
        assert(type(instr) == Instruction)
        for i, d in enumerate(instr.wdat):
            assert(d == Bits(hex='0xAA', length=32))

    # @unittest.skip("Skipping while singleLoadHit isn't working")
    def test_singleLoadMiss(self):
        mshr_addrs = []
        instr = self.genLoad(pc=0, rd=0, rdat1 = [Bits(int=i, length=32) for i in range(0, 0x400, 32)])
        self.issue_if.push(instr)
        self.ldst_fu.tick()
        
        miss_count = 0
        while miss_count < 8:
            if self.dcache_if.valid:
                mshr_addrs.append(self.genMiss()) # [tuple(int, int)]
                miss_count += 1
            else:
                self.dcache_fwd.push(None)
            self.ldst_fu.tick()
        
        while len(mshr_addrs) > 0:
            mshr_addr = mshr_addrs.pop(0)
            self.mshrHit(mshr_addr, '0xAA')
            self.ldst_fu.tick()
        
        self.dcache_fwd.push(None)
        self.ldst_fu.tick()
        
        assert(self.wb_if.valid)
        
        for i, d in enumerate(instr.wdat):
            assert(d == Bits(hex='0xAA', length=32))
    
    def test_singlePredHit(self):
        pred = [Bits(bin='0b0') for i in range(32)]
        pred[0] = Bits(bin='0b1')
        instr = self.genLoad(pc=0, rd=0, rdat1 = [Bits(int=i, length=32) for i in range(0, 0x400, 32)], pred=pred)
        self.issue_if.push(instr)
        self.ldst_fu.tick()

        hit_count = 0
        while not self.wb_if.valid:
            if self.dcache_if.valid:
                self.genHit('0xAA')
                hit_count += 1
            else:
                self.dcache_fwd.push(None)
            self.ldst_fu.tick()
        
        assert(hit_count == 1)

if __name__ == '__main__':
    unittest.main()