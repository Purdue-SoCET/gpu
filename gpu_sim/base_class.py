#!/usr/bin/env python3
"""Small base class and an executable CLI entrypoint.

This module provides a tiny BaseClass used for demonstration and a
convenient `main()` function so the file can be executed directly.

Features added:
- BaseClass with a simple `process()` method
- `argparse` based CLI with `--name` and `--repeat` options
- basic `logging` configuration

Run with: python -m src.base_class --name Alice --repeat 3
"""

from __future__ import annotations

import argparse
import logging
import struct
import sys
from dataclasses import dataclass
from typing import Optional
from unicodedata import name

@dataclass
class tb_data_params:
	gridX_dim: int
	gridY_dim: int
	gridZ_dim: int
	blockX_dim: int
	blockY_dim: int
	blockZ_dim: int
	

@dataclass
class StageInterface:
    """Represents the handshake and data path between two pipeline stages."""

    def __init__(self, name, latency=1):
        self.name = name
        self.latency = latency

        # Current and next-cycle values
        self.data = None
        self.next_data = None

        # Control signals
        self.valid = False
        self.next_valid = False
        self.ready = True      # downstream can accept
        self.stall = False

        # Timing
        self.remaining_latency = 0

    # -------------------------------------------------------
    # Data / control manipulation
    # -------------------------------------------------------
    def send(self, data):
        """Upstream stage pushes data into this interface."""
        if not self.ready:
            self.stall = True
            return False
        self.next_data = data
        self.next_valid = True
        self.remaining_latency = self.latency
        return True

    def receive(self):
        """Downstream stage consumes data if valid and latency done."""
        if self.valid and self.remaining_latency <= 0:
            d = self.data
            self.data = None
            self.valid = False
            self.ready = True
            return d
        return None

    def flush(self):
        """Clear any in-flight data (e.g., on branch mispredict)."""
        self.data = None
        self.next_data = None
        self.valid = self.next_valid = False
        self.remaining_latency = 0
        self.stall = False
        self.ready = True

    # -------------------------------------------------------
    # Cycle transition
    # -------------------------------------------------------
    def tick(self):
        """Advance one cycle of timing and commit next values."""
        if self.remaining_latency > 0:
            self.remaining_latency -= 1

        # Commit next values at cycle boundary
        if self.next_valid:
            self.data = self.next_data
            self.valid = True
            self.ready = False  # data now occupied
        else:
            # If nothing new is sent and latency expired, free the latch
            if not self.valid:
                self.ready = True

        # Clear transient signals
        self.next_data = None
        self.next_valid = False
        self.stall = False

    def can_accept(self) -> bool:
        """Return True if this interface can accept a new push from upstream.

        Definition of "can accept":
        - interface is marked ready (downstream not currently holding data)
        - nothing is already scheduled for the next cycle (next_valid is False)
        - no remaining latency is active (data path is free)
        """
        return bool(self.ready and not self.next_valid and self.remaining_latency <= 0)


@dataclass
class SoCET_GPU():
	"""A minimal base class used for demos and tests.

	Attributes:
		name: The name to process.
		times: How many times to repeat the greeting.
	"""

	def __init__(self, name: str = "World", times: int = 1):
		self.name = "SoCET GPU"
		self.semester = "F25"
		self.version = "0.1.0"

from dataclasses import dataclass

@dataclass
class SM():
    """Streaming Multiprocessor (SM) containing a simple scalar pipeline."""

    def __init__(self):
        # create the interfaces
        self.if_scheduler_fetch = StageInterface("IF_SchedulerFetch", latency=1)
        self.if_fetch_decode = StageInterface("IF_FetchDecode", latency=1)
        self.if_decode_exec  = StageInterface("IF_DecodeExec", latency=1)
        self.if_exec_wb      = StageInterface("IF_ExecWriteback", latency=1)

        # creates the stages
        self.warp_scheduler = PipelineStage("WarpScheduler", self)
        self.fetch     = PipelineStage("Fetch", self)
        self.decode    = PipelineStage("Decode", self)
        self.execute   = PipelineStage("Execute", self)
        self.writeback = PipelineStage("Writeback", self)

        # connect 
        self.warp_scheduler.connect_output(self.if_scheduler_fetch)
        self.fetch.connect_input(self.if_scheduler_fetch)
        self.fetch.connect_output(self.if_fetch_decode)
        self.decode.connect_input(self.if_fetch_decode)
        self.decode.connect_output(self.if_decode_exec)
        self.execute.connect_input(self.if_decode_exec)
        self.execute.connect_output(self.if_exec_wb)
        self.writeback.connect_input(self.if_exec_wb)

        #ordered list of the stages
        self.stages = [self.warp_scheduler, self.fetch, self.decode, self.execute, self.writeback]
        self.interfaces = [self.if_scheduler_fetch, self.if_fetch_decode, self.if_decode_exec, self.if_exec_wb]

        self.global_cycle = 0
        self.completed_insts = 0

    def cycle(self):
        """Run one simulation cycle (back-to-front)."""
        self.global_cycle += 1

        # 1. Advance timing in all interfaces (latency countdown)
        for iface in self.interfaces:
            iface.tick()

        # 2. Run pipeline stages in back-to-front order
        for stage in reversed(self.stages):
            stage.cycle()

        # 3. Gather metrics (optional)
        for stage in self.stages:
            self.completed_insts += stage.instruction_count

    def print_pipeline_state(self):
        print(f"=== Cycle {self.global_cycle} ===")
        for iface in self.interfaces:
            state = (
                f"[{iface.name}] valid={iface.valid}, "
                f"ready={iface.ready}, "
                f"latency_left={iface.remaining_latency}, "
                f"data={iface.data}"
            )
            print(state)
        print()

@dataclass
class TB_Scheduler:
	def __init__(self):
		self.num_threads = 32
		self.gridX_dim = 32
		# tb_data_params expects (gridX_dim, gridY_dim, gridZ_dim, blockX_dim, blockY_dim, blockZ_dim)
		self.data_params_struct = tb_data_params(
			gridX_dim=32,
			gridY_dim=32,
			gridZ_dim=1,
			blockX_dim=32,
			blockY_dim=32,
			blockZ_dim=1,
		)
		self.data_address = 0x000
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PipelineStage:
    name: str
    parent_core: object

    input_if: Optional["StageInterface"] = None
    output_if: Optional["StageInterface"] = None

    subunits: list = field(default_factory=list)

    # Performance metadata
    cycle_count: int = 0
    active_cycles: int = 0
    stall_cycles: int = 0
    instruction_count: int = 0

    # ---------------------------------------------------------
    # Connectivity
    # ---------------------------------------------------------
    def connect_input(self, interface: "StageInterface") -> None:
        """Bind an incoming interface to this stage."""
        self.input_if = interface

    def connect_output(self, interface: "StageInterface") -> None:
        """Bind an outgoing interface to this stage."""
        self.output_if = interface

    def add_subunit(self, fu) -> None:
        """Attach a sub-functional unit (ALU, LSU, etc.)."""
        self.subunits.append(fu)

    # ---------------------------------------------------------
    # Simulation Cycle
    # ---------------------------------------------------------
    def cycle(self) -> None:
        """Advance one cycle with handshake-based data flow."""
        self.cycle_count += 1
        received_inst = None

        # 1. Try to receive instruction from input interface
        if self.input_if:
            received_inst = self.input_if.receive()

        if received_inst:
            self.active_cycles += 1
            result = self.process(received_inst)

            # 2. Attempt to send to output interface, but only if downstream can accept
            if self.output_if and result is not None:
                if self.output_if.can_accept():
                    sent = self.output_if.send(result)
                    if not sent:
                        # Downstream not ready → stall
                        self.stall_cycles += 1
                        self.active_cycles -= 1  # didn’t complete
                else:
                    # Downstream cannot accept this cycle → stall
                    self.stall_cycles += 1
                    self.active_cycles -= 1
        else:
            self.stall_cycles += 1

    # ---------------------------------------------------------
    # Readiness helpers
    # ---------------------------------------------------------
    def accepting_input(self) -> bool:
        """Return True if this stage's input interface can accept new data now."""
        return bool(self.input_if and self.input_if.can_accept())

    def can_forward_output(self) -> bool:
        """Return True if this stage can forward data to its output this cycle."""
        return bool(self.output_if and self.output_if.can_accept())

    def process(self, inst):
        """Override per-stage with functional behavior."""
        # Default: simple pass-through
        return inst

    def stats(self):
        return {
            "name": self.name,
            "cycles": self.cycle_count,
            "active": self.active_cycles,
            "stalls": self.stall_cycles,
            "utilization": (
                self.active_cycles / self.cycle_count if self.cycle_count else 0.0
            ),
        }

            
class DecodeStage(PipelineStage):
    def __init__(self, parent_core):
        super().__init__("Decode", parent_core)
        self.flush_flag = False
        self.halt = False

    def connect_interfaces(self, input_if: "StageInterface", output_if: "StageInterface"):
        self.connect_input(input_if)
        self.connect_output(output_if)

    def process(self, inst):
        if not inst:
            return None

        # Interpret instruction as a 32-bit integer and extract the low 7-bit opcode.
        raw = int(inst.get("raw", 0)) & 0xFFFFFFFF
        opcode_upper = raw & 0x7  # bits 6-3
        opcode_lower = (raw >> 3) & 0xF  # bits 2-0
        opcode_r0_dict = {
            "000": "add",
            "001": "sub",
            "010": "mul",
            "011": "div",
            "100": "and",
            "101": "or",
            "110": "xor",
            "111": "slt",
        }
        opcode_r1_dict = {
            "000": "sltu",
            "001": "addf",
            "010": "subf",
            "011": "mulf",
            "100": "divf",
            "101": "sll",
            "110": "srl",
            "111": "sra",
        }
        opcode_i0_dict = {
            "000": "addi",
            "001": "subi",
            "101": "ori",
            "111": "slti",
        }
        opcode_i1_dict = {
            "000": "sltiu",
            "001": "srli",
            "101": "srai",
        }
        opcode_i2_dict = {
            "000": "lw",
            "001": "st",
            "010": "lb",
            "011": "jalr"
        }

        def sign_extend(value: int, bits: int) -> int:
            sign_bit = 1 << (bits - 1)
            return (value & (sign_bit - 1)) - (value & sign_bit)

        # Field extraction according to the provided ISA layout
        opcode7 = raw & 0x7F
        rd = (raw >> 7) & 0x3F
        rs1 = (raw >> 13) & 0x3F
        # bits [24:19] used either as rs2 (6 bits) or imm field depending on type
        mid6 = (raw >> 19) & 0x3F
        pred = (raw >> 25) & 0x1F
        packet_start = bool((raw >> 30) & 0x1)
        packet_end = bool((raw >> 31) & 0x1)

        high4 = (opcode7 >> 3) & 0xF
        low3 = opcode7 & 0x7

        # Build opcode -> mnemonic map from the provided table (subset implemented)
        opcode_map = {
            # R-type (high4 = 0b0000)
            0b0000000: "add",
            0b0000001: "sub",
            0b0000010: "mul",
            0b0000011: "div",
            0b0000100: "and",
            0b0000101: "or",
            0b0000110: "xor",
            0b0000111: "slt",
            # R-type / FP and shifts (high4 = 0b0001)
            0b0001000: "sltu",  # 0001 000 -> 8
            0b0001001: "addf",
            0b0001010: "subf",
            0b0001011: "mulf",
            0b0001100: "divf",
            0b0001101: "sll",
            0b0001110: "srl",
            0b0001111: "sra",
            # I-type (0010, 0011)
            0b0010000: "addi",
            0b0010001: "subi",
            0b0010101: "ori",
            0b0010111: "slti",
            0b0011000: "sltiu",  # 0011 000 -> 24
            0b0011110: "srli",
            0b0011111: "srai",
            0b0100000: "lw",    # 0100 000 -> 32
            0b0100001: "lh",
            0b0100010: "lb",
            0b0100011: "jalr",
            # F-type (0101)
            0b0101000: "isqrt",
            0b0101001: "sin",
            0b0101010: "cos",
            0b0101011: "itof",
            0b0101100: "ftoi",
            # S-type (0110)
            0b0110000: "sw",
            0b0110001: "sh",
            0b0110010: "sb",
            # B-type (1000)
            0b1000000: "beq",
            0b1000001: "bne",
            0b1000010: "bge",
            0b1000011: "bgeu",
            0b1000100: "blt",
            0b1000101: "bltu",
            # U-type (1010)
            0b1010000: "auipc",
            0b1010001: "lli",
            0b1010010: "lmi",
            0b1010100: "lui",
            # C-type (1011)
            0b1011000: "csrr",
            0b1011001: "csrw",
            # J-type (1100)
            0b1100000: "jal",
            # P-type (1101)
            0b1101000: "jpnz",
            # H-type: halt is all ones (0b1111111 -> 127)
            0b1111111: "halt",
        }

        mnemonic = opcode_map.get(opcode7, "nop")

        # Interpret fields according to determined instruction class (best-effort)
        decoded: dict = {
            "raw": raw,
            "opcode7": opcode7,
            "mnemonic": mnemonic,
            "predication": pred,
            "packet_start": packet_start,
            "packet_end": packet_end,
        }

        # Classify by high4 nibble
        if high4 in (0x0, 0x1):
            # R-type family (register-register)
            decoded.update({"type": "R", "rd": rd, "rs1": rs1, "rs2": mid6})
        elif high4 in (0x2, 0x3, 0x4):
            # I-type family (immediates and loads/jalr)
            imm6 = sign_extend(mid6, 6)
            decoded.update({"type": "I", "rd": rd, "rs1": rs1, "imm": imm6})
        elif high4 == 0x5:
            # F-type / unary ops: rd, rs1
            decoded.update({"type": "F", "rd": rd, "rs1": rs1})
        elif high4 in (0x6, 0x7):
            # S-type family (store / memory write)
            decoded.update({"type": "S", "imm": mid6, "rs1": rs1, "rs2": rd})
        elif high4 == 0x8:
            # B-type (branch): preddest in rd field
            decoded.update({"type": "B", "pred_dest": rd, "rs1": rs1, "rs2": mid6})
        elif high4 == 0xA:
            # U-type: 12-bit immediate occupies bits [24:13]
            imm12 = (raw >> 13) & 0xFFF
            decoded.update({"type": "U", "rd": rd, "imm12": sign_extend(imm12, 12)})
        elif high4 == 0xB:
            # C-type: CSR op
            decoded.update({"type": "C", "rd": rd, "csr": (raw >> 13) & 0x3FF})
        elif high4 == 0xC:
            # J-type: jal
            imm12 = (raw >> 13) & 0xFFF
            decoded.update({"type": "J", "rd": rd, "imm12": sign_extend(imm12, 12)})
        elif high4 == 0xD:
            # P-type: predicated jump
            decoded.update({"type": "P", "rs1": rs1, "rs2": mid6})
        elif opcode7 == 0x7F:
            decoded.update({"type": "H", "mnemonic": "halt"})
        else:
            decoded.update({"type": "UNKNOWN"})

        # Attach the original instruction for reference
        decoded["orig_inst"] = inst

        return {"decoded": True, "decoded_fields": decoded}

    def flush(self):
        """Flush the stage and its interfaces."""
        if self.input_if:
            self.input_if.flush()
        if self.output_if:
            self.output_if.flush()
        self.flush_flag = True

    def debug_state(self):
        return {
            "name": self.name,
            "flush_flag": self.flush_flag,
            "halt": self.halt,
        }
     

# class faux_SM():

def make_raw(op7: int, rd: int = 1, rs1: int = 2, mid6: int = 3, pred: int = 0, packet_start: bool = False, packet_end: bool = False) -> int:
    """Construct a 32-bit instruction word according to the DecodeStage layout:
    bits [6:0]   = opcode7
    bits [12:7]  = rd (6)
    bits [18:13] = rs1 (6)
    bits [24:19] = mid6 (6)
    bits [29:25] = pred (5)
    bit  [30]    = packet_start
    bit  [31]    = packet_end
    """
    raw = (
        (int(packet_end) << 31)
        | (int(packet_start) << 30)
        | ((pred & 0x1F) << 25)
        | ((mid6 & 0x3F) << 19)
        | ((rs1 & 0x3F) << 13)
        | ((rd & 0x3F) << 7)
        | (op7 & 0x7F)
    )
    return raw


#--------------------------------------------------------
# THIS IS A SAMPLE CODE SEQUENCE TO TEST THE DECODER.
# REPLACE WITH NAMING FOR YOUR UNIT CLASS NAME AS NEEDED.
#--------------------------------------------------------
# Build a small sequence of instructions that align with the decoder's expected opcode values
# test_in = StageInterface("IF_FetchDecode", latency=1)
# test_out = StageInterface("IF_DecodeExec", latency=1)
# decode = DecodeStage("SM_1")
# decode.connect_interfaces(test_in, test_out)
# 
# UNCOMMENT THIS WHEN YOU'RE READY TO TEST!
# THIS IS NOT A CYCLE ACCURATE SIM JUST YET--JUST FUNCTIONAL. 
# SM MODULE FOR SIMULATING CYCLE ACCURATE PROCESSES IS IN PROGRESS.
# instructions = [
#     {"pc": 0x100, "raw": make_raw(0x00, rd=1, rs1=2, mid6=3)},    # add (R-type)
#     {"pc": 0x104, "raw": make_raw(0x10, rd=5, rs1=6, mid6=0)},    # addi (I-type)
#     {"pc": 0x108, "raw": make_raw(0x20, rd=2, rs1=3, mid6=4)},    # lw  (I-type / load)
#     {"pc": 0x10C, "raw": make_raw(0x30, rd=2, rs1=3, mid6=4)},    # sw  (S-type)
#     {"pc": 0x110, "raw": make_raw(0x40, rd=0, rs1=1, mid6=2, pred=1, packet_start=True)},  # beq (B-type) with packet start
#     {"pc": 0x114, "raw": make_raw(0x7F, rd=0, rs1=0, mid6=0)},    # halt (H-type)
# ]

for inst in instructions:
    print(f"\nIssuing instruction pc=0x{inst['pc']:x} raw=0x{inst['raw']:08x}")
    
    # Wait until decode can accept a new one
    while not test_in.can_accept():
        test_in.tick()
        test_out.tick()
        decode.cycle()

    # Send and advance one cycle
    test_in.send(inst)
    test_in.tick()
    test_out.tick()
    
    #REPLACE WITH YOUR UNIT CLASS.cycle()
    #EX. decode.cycle()

    # Next cycle: promote and observe decode output
    test_in.tick()
    test_out.tick()
    decode.cycle()

    print(f"Output IF: valid={test_out.valid}, ready={test_out.ready}, data={test_out.data}")