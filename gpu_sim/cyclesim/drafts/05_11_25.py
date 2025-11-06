from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from collections import deque

###TEST CODE BELOW###

@dataclass
class Warp:
    pc: int
    group_id: int
    can_issue: bool = True
    halt: bool = True

@dataclass
class Instruction:
    # init members
    pc: int
    warp: int
    warpGroup: int
    
    # instruction
    opcode: int
    rs1: int
    rs2: int
    rd: int
    pred: int
    packet: # assume packet is some 


    # for perf
    issued_cycle: Optional[int] = None
    stage_entry: Dict[str, int] = field(default_factory=dict)   # stage -> first cycle seen
    stage_exit:  Dict[str, int] = field(default_factory=dict)   # stage -> last cycle completed
    fu_entries:  List[Dict]     = field(default_factory=list)   # [{fu:"ALU", enter: c, exit: c}, ...]
    wb_cycle: Optional[int] = None

    def mark_stage_enter(self, stage: str, cycle: int):
        self.stage_entry.setdefault(stage, cycle)

    def mark_stage_exit(self, stage: str, cycle: int):
        self.stage_exit[stage] = cycle

    def mark_fu_enter(self, fu: str, cycle: int):
        self.fu_entries.append({"fu": fu, "enter": cycle, "exit": None})

    def mark_fu_exit(self, fu: str, cycle: int):
        for e in reversed(self.fu_entries):
            if e["fu"] == fu and e["exit"] is None:
                e["exit"] = cycle
                return

    def mark_writeback(self, cycle: int):
        self.wb_cycle = cycle

@dataclass
class ForwardingIF:
    payload: Optional[Any] = None
    valid: bool = False
    wait: bool = False
    name: str = field(default="BackwardIF", repr=False)

    def push(self, data: Any) -> bool:
        if self.valid:
            return False
        self.payload = data
        self.valid = True
    
    def force_push(self, data: Any) -> None:
        self.payload = data
        self.valid = True

    def snoop(self) -> Optional[Any]:
        return self.payload if self.valid else None
    
    def pop(self) -> Optional[Any]:
        if not self.valid:
            return None
        data = self.payload
        self.payload = None
        self.valid = False
        return data
    
    def set_wait(self, flag: bool) -> None:
        self.wait = bool(flag)

    def clear_all(self) -> None:
        self.payload = None
        self.valid = False
        self.wait = False

    def __repr__(self) -> str:
        return (f"<{self.name} valid={self.valid} wait={self.wait} "
            f"payload={self.payload!r}>")

  
@dataclass
class LatchIF:
    payload: Optional[Any] = None
    valid: bool = False
    read: bool = False
    name: str = field(default="LatchIF", repr=False)
    forward_if: Optional[ForwardingIF] = None

    def ready_for_push(self) -> bool:
        if self.valid:
            return False
        if self.forward_if is not None and self.forward_if.wait:
            return False
        return True

    def push(self, data: Any) -> bool:
        if not self.ready_for_push():
            return False
        self.payload = data
        self.valid = True
        return True
    
    def force_push(self, data: Any) -> None: # will most likely need a forceful push for squashing
        self.payload = data
        self.valid = True

    def snoop(self) -> Optional[Any]: # may need this if we want to see the data without clearing the data
        return self.payload if self.valid else None
    
    def pop(self) -> Optional[Any]:
        if not self.valid:
            return None
        data = self.payload
        self.payload = None
        self.valid = False
        return data
    
    def clear_all(self) -> None:
        self.payload = None
        self.valid = False
    
    def __repr__(self) -> str: # idk if we need this or not
        return (f"<{self.name} valid={self.valid} wait={self.wait} "
                f"payload={self.payload!r}>")
  
    
@dataclass
class Stage:
    name: str
    behind_latch: Optional[LatchIF] = None
    ahead_latch: Optional[LatchIF] = None
    forward_if: Optional[List[ForwardingIF]] = field(default_factory=list)

    def has_input(self) -> bool:
        if self.behind_latch is None: 
            # no behind latch, so always assume true
            return True
        return self.behind_latch.valid
    
    def get_input(self) -> Optional[Any]:
        if self.behind_latch is None:
            # no behind latch, so pop nothing
            return None
        return self.behind_latch.pop()
    
    def can_output(self) -> bool:
        if self.ahead_latch is None:
            return True
        if self.ahead_latch.forward_if:
            # If the ahead latch has one or more forward paths, stall if any are waiting
            if isinstance(self.ahead_latch.forward_if, list):
                if any(f.wait for f in self.ahead_latch.forward_if):
                    return False
            elif self.ahead_latch.forward_if.wait:
                return False
        return self.ahead_latch.ready_for_push()
    
    def send_output(self, data: Any) -> None:
        if self.ahead_latch is None:
            print(f"[{self.name}] Done: {data!r}")
        else:
            if self.ahead_latch.ready_for_push():
                self.ahead_latch.push(data)
            else:
                print(f"[{self.name}] Could not push output — next stage not ready.")

    def snoop_forwards(self) -> List[Any]:
        """Collect snooped values from all forward interfaces."""
        values = []
        if not self.forward_ifs:
            return values
        for f in self.forward_ifs:
            if f and f.valid:
                values.append(f.snoop())
        return values

    def compute(self, input_data: Any) -> Any:
        # default computation, subclassess will override this
        return input_data

    def step(self) -> None:
        if not self.can_output():
            print(f"[{self.name}] Stalled — next stage not ready.")
            return
        
        if not self.has_input():
            print(f"[{self.name}] No input available, idle this cycle.")
            return
        
        input_data = self.get_input()
        output_data = self.compute(input_data)
        self.send_output(output_data)

FetchDecodeIF = LatchIF(name = "FetchDecodeIF")
DecodeIssue_IbufferIF = LatchIF(name = "DecodeIIF")  
de_sched_EOP = ForwardingIF(name = "Decode_Scheduler_EOP")
de_sched_EOP_WID = ForwardingIF(name = "Decode_Scheduler_WARPID")
de_sched_BARR = ForwardingIF(name = "Deecode_Schedular_BARRIER")
de_sched_B_WID = ForwardingIF(name = "Decode_Scheduler_BARRIER_WARPID")
de_sched_B_GID = ForwardingIF(name = "Decode_Scheduler_BARRIER_GROUPID")
de_sched_B_PC = ForwardingIF(name = "Decode_Scheduler_BARRIER_PC")
icache_de_ihit = ForwardingIF(name = "ICache_Decode_Ihit")

# @dataclass
# class FU():
#     name = 
class BranchFU:
    def __init__(self, instructions: Instruction, prf_rd_data, op_1, op_2):
        self.warp_id = instructions.warp
        self.decode_mapping_table = {
            0: "beq",
            1: "bne",
            2: "bge",
            3: "bgeu",
            4: "blt",
            5: "bltu",
        }
        self.opcode = self.decode_mapping_table[instructions.opcode]
        self.prf_rd_data = prf_rd_data
        self.op1 = op_1
        self.op2 = op_2
        self.num_threads = len(op_1)
        self.prf_wr_data = None

    def to_signed(self, val, bits=32):
        if val & (1 << (bits - 1)):
            val -= 1 << bits
        return val

    def alu_decoder(self):
        if self.opcode == "beq":
            results = [self.op1[i] == self.op2[i] for i in range(self.num_threads)]
        elif self.opcode == "bne":
            results = [self.op1[i] != self.op2[i] for i in range(self.num_threads)]
        elif self.opcode == "bge":
            results = [self.to_signed(self.op1[i]) >= self.to_signed(self.op2[i]) for i in range(self.num_threads)]
        elif self.opcode == "bgeu":
            results = [self.op1[i] >= self.op2[i] for i in range(self.num_threads)]
        elif self.opcode == "blt":
            results = [self.to_signed(self.op1[i]) < self.to_signed(self.op2[i]) for i in range(self.num_threads)]
        elif self.opcode == "bltu":
            results = [self.op1[i] < self.op2[i] for i in range(self.num_threads)]
        else:
            raise ValueError(f"Unknown opcode {self.opcode}")
        return results

    def update_pred(self):
        tnt = self.alu_decoder()
        self.prf_wr_data = [
            self.prf_rd_data[i] and tnt[i] for i in range(self.num_threads)
        ]
        return self.prf_wr_data
 
class PredicateRegFile():
    def __init__(self, num_preds_per_warp: int, num_warps: int):
        num_cols = num_preds_per_warp *2 # the number of 
        num_threads = 32

        # 2D structure: warp -> predicate -> [bits per thread]
        self.reg_file = [
            [[[False] * self.num_threads, [False] * self.num_threads]
              for _ in range(num_cols)]
            for _ in range(num_warps)
        ]
    
    def read_predicate(self, prf_rd_en: int, prf_rd_wsel: int, prf_rd_psel: int, prf_neg: int):
        "Predicate register file reads by selecting a 1 from 32 warps, 1 from 16 predicates,"
        " and whether it wants the inverted version or not..."

        if (prf_rd_en):
            return self.reg_file[prf_rd_wsel][prf_rd_psel][prf_neg]
        else: 
            return None
    
    def write_predicate(self, prf_wr_en, prf_wr_wsel: int, prf_wr_psel: int, prf_wr_data):
        # the write will autopopulate the negated version in the table)
        if (prf_wr_en):
                # Convert int to bit array if needed
            if isinstance(prf_wr_data, int):
                bits = [(prf_wr_data >> i) & 1 == 1 for i in range(self.num_threads)]
            else:
                bits = prf_wr_data  # assume already a list of bools

            # Store positive version
            self.reg_file[prf_wr_wsel][prf_wr_psel][0] = bits
            # Store negated version
            self.reg_file[prf_wr_wsel][prf_wr_psel][1] = [not b for b in bits]

class DecodeStage(Stage):
    def __init__(self, instructions: Instruction, prf: PredicateRegFile):
        self.name = "Decode"
        self.behind_latch = FetchDecodeIF
        self.ahead_latch = DecodeIssue_IbufferIF
        self.forward_if: [de_sched_EOP,       # end-of-packet flag
            de_sched_EOP_WID,   # warp ID at EOP
            de_sched_BARR,      # barrier synchronization flag
            de_sched_B_WID,     # warp ID for barrier
            de_sched_B_GID,     # group ID for barrier
            de_sched_B_PC, 
            icache_de_ihit
        ] 
        self.inst = instructions
        self.prf = prf
        # YOUR job to populate the opcode, rs1, rs2, rd, pred, packet...


    def compute(self, input_data: Any) -> Any:
        if input_data is None:
            return None
                
        if self.forward_if and self.forward_if.wait:
            print(f"[{self.name}] Stalled due to wait from next stage.")
            return None
                
        fwd_val = self.forward_if.snoop() if self.forward_if else None
        if fwd_val is not None: # actual logic 
            # time to do actual stuff!

            raw_field = self.inst.packet
            if isinstance(raw_field, str):
                raw = int(raw_field, 0) & 0xFFFFFFFF      # handle "0x..." or decimal string
            elif isinstance(raw_field, list):
                raw = 0
                for i, byte in enumerate(raw_field):
                    raw |= (byte & 0xFF) << (8 * i)
                raw &= 0xFFFFFFFF
            else:
                raw = int(raw_field) & 0xFFFFFFFF

            # --- extract fields ---
            opcode7 = raw & 0x7F
            rd = (raw >> 7) & 0x3F
            rs1 = (raw >> 13) & 0x3F
            mid6 = (raw >> 19) & 0x3F
            pred = (raw >> 25) & 0x1F
            packet_start = bool((raw >> 30) & 0x1)
            packet_end = bool((raw >> 31) & 0x1)

            def sign_extend(value: int, bits: int) -> int:
                sign_bit = 1 << (bits - 1)
                return (value & (sign_bit - 1)) - (value & sign_bit)

            high4 = (opcode7 >> 3) & 0xF

            opcode_map = {
                0b0000000: "add",
                0b0000001: "sub",
                0b0000010: "mul",
                0b0000011: "div",
                0b0000100: "and",
                0b0000101: "or",
                0b0000110: "xor",
                0b0000111: "slt",
                0b0001000: "sltu",
                0b0001001: "addf",
                0b0001010: "subf",
                0b0001011: "mulf",
                0b0001100: "divf",
                0b0001101: "sll",
                0b0001110: "srl",
                0b0001111: "sra",
                0b0010000: "addi",
                0b0010001: "subi",
                0b0010101: "ori",
                0b0010111: "slti",
                0b0011000: "sltiu",
                0b0011110: "srli",
                0b0011111: "srai",
                0b0100000: "lw",
                0b0100001: "lh",
                0b0100010: "lb",
                0b0100011: "jalr",
                0b0101000: "isqrt",
                0b0101001: "sin",
                0b0101010: "cos",
                0b0101011: "itof",
                0b0101100: "ftoi",
                0b0110000: "sw",
                0b0110001: "sh",
                0b0110010: "sb",
                0b1000000: "beq",
                0b1000001: "bne",
                0b1000010: "bge",
                0b1000011: "bgeu",
                0b1000100: "blt",
                0b1000101: "bltu",
                0b1010000: "auipc",
                0b1010001: "lli",
                0b1010010: "lmi",
                0b1010100: "lui",
                0b1011000: "csrr",
                0b1011001: "csrw",
                0b1100000: "jal",
                0b1101000: "jpnz",
                0b1111111: "halt",
            }

            mnemonic = opcode_map.get(opcode7, "nop")
            self.inst.opcode = mnemonic
            self.inst.rs1 = rs1
            self.inst.rs2 = mid6
            self.inst.rd = rd
            
            pred_mask = self.prf.read_predicate(prf_rd_en=1, prf_rd_wsel=self.inst.warp, prf_rd_psel=pred, prf_neg=0)

            if pred_mask is None:
                pred_mask = [True] *32
            
            self.inst.pred = pred_mask
            return self.inst 
        
## TEST INIT CODE BELOW ##

# --- Prerequisites ---
# Assuming DecodeStage, Instruction, PredicateRegFile, LatchIF, ForwardingIF are all imported

def make_test_pipeline():
    """Helper to build a test decode stage pipeline setup."""
    prf = PredicateRegFile(num_preds_per_warp=4, num_warps=2)
    
    # Preload predicate registers for warp 0
    prf.write_predicate(prf_wr_en=1, prf_wr_wsel=0, prf_wr_psel=0,
                        prf_wr_data=[True, False] * 16)  # alternating pattern

    # Create decode stage and interfaces
    inst = Instruction(pc=0x100, warp=0, warpGroup=0,
                       opcode=0, rs1=0, rs2=0, rd=0, pred=0, packet=None)
    decode_stage = DecodeStage(inst, prf)

    # Setup pipeline latches
    FetchDecodeIF.clear_all()
    DecodeIssue_IbufferIF.clear_all()

    # Connect decode's behind and ahead latches
    decode_stage.behind_latch = FetchDecodeIF
    decode_stage.ahead_latch = DecodeIssue_IbufferIF

    return decode_stage, inst, prf

def test_rtype_instruction():
    decode, inst, prf = make_test_pipeline()

    inst.packet = "0x0000190D89"  # add-like
    FetchDecodeIF.force_push(inst)
    decode.step()

    decoded_out = DecodeIssue_IbufferIF.pop()
    assert decoded_out is not None
    print("[R-Type] Decoded:", decoded_out)
    assert decoded_out.opcode != 0
    assert decoded_out.rs1 != 0
    assert decoded_out.rs2 != 0
    assert isinstance(decoded_out.pred, list)
    assert len(decoded_out.pred) == 32


def test_load_instruction():
    decode, inst, prf = make_test_pipeline()
    inst.packet = "0x0200112090"  # lw-like
    FetchDecodeIF.force_push(inst)
    decode.step()
    decoded_out = DecodeIssue_IbufferIF.pop()
    assert decoded_out.opcode != 0
    assert decoded_out.rs1 == (int("0x0200112090", 16) >> 13) & 0x3F
    print("[I-Type Load] Decoded:", decoded_out)


def test_store_instruction():
    decode, inst, prf = make_test_pipeline()
    inst.packet = "0x03001928C0"  # sw-like
    FetchDecodeIF.force_push(inst)
    decode.step()
    decoded_out = DecodeIssue_IbufferIF.pop()
    print("[S-Type Store] Decoded:", decoded_out)
    assert decoded_out.rs1 != 0
    assert decoded_out.rs2 != 0


def test_branch_instruction():
    decode, inst, prf = make_test_pipeline()
    inst.packet = "0x0800190980"  # beq-like
    FetchDecodeIF.force_push(inst)
    decode.step()
    decoded_out = DecodeIssue_IbufferIF.pop()
    print("[B-Type Branch] Decoded:", decoded_out)
    assert decoded_out.opcode != 0
    assert isinstance(decoded_out.pred, list)


def test_jump_instruction():
    decode, inst, prf = make_test_pipeline()
    inst.packet = "0x0C00080900"  # jal-like
    FetchDecodeIF.force_push(inst)
    decode.step()
    decoded_out = DecodeIssue_IbufferIF.pop()
    print("[J-Type Jump] Decoded:", decoded_out)
    assert decoded_out.opcode != 0
    assert decoded_out.rd != 0

def test_wait_on_ihit_false():
    decode, inst, prf = make_test_pipeline()

    # Simulate ICache miss (ihit=False)
    icache_de_ihit.force_push(False)

    inst.packet = "0x0000190D89"
    FetchDecodeIF.force_push(inst)
    decode.step()

    # Decode should stall → not push to next stage
    assert not DecodeIssue_IbufferIF.valid
    print("[ForwardIF] Correctly stalled on ihit=False")


def test_ready_on_ihit_true():
    decode, inst, prf = make_test_pipeline()

    icache_de_ihit.force_push(True)  # ihit=True
    inst.packet = "0x0000190D89"
    FetchDecodeIF.force_push(inst)
    decode.step()

    # Should have forwarded decode result
    assert DecodeIssue_IbufferIF.valid
    print("[ForwardIF] Correctly forwarded on ihit=True")


def test_set_outgoing_wait_and_clear():
    decode, inst, prf = make_test_pipeline()
    decode.set_outgoing_wait()
    assert any(f.wait for f in decode.outgoing_ifs)
    decode.clear_outgoing()
    assert all(not f.wait and not f.valid for f in decode.outgoing_ifs)
    print("[ForwardIF] Wait/Clear verified")

if __name__ == "__main__":
    test_rtype_instruction()
    test_load_instruction()
    test_store_instruction()
    test_branch_instruction()
    test_jump_instruction()
    test_wait_on_ihit_false()
    test_ready_on_ihit_true()
    test_set_outgoing_wait_and_clear()
    print("\n✅ All DecodeStage tests passed.")
