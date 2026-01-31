import sys
from pathlib import Path
gpu_root = Path(__file__).resolve().parents[4]
sys.path.append(str(gpu_root))
sys.path.insert(0,str(gpu_root))
print(sys.path)

from common.custom_enums_multi import Instr_Type, R_Op, I_Op, F_Op, S_Op, B_Op, U_Op, J_Op, P_Op, H_Op
from common.custom_enums import Op
from simulator.src.decode.decode_class import DecodeStage, decode_opcode, classify_fust_unit
from simulator.src.decode.predicate_reg_file import PredicateRegFile
from simulator.src.mem.icache_stage import ICacheStage 
from simulator.base_class import *
from bitstring import Bits


def setup_connections():
    # Setup latches and interfaces 

    # entry latch that gets requests from the warp scheduler 
    sched_icache_latch = LatchIF("Sched-Decode Latch") 
    # exit latch that sends the populated instruction class into the following stages.
    decode_issue_latch = LatchIF("Decode-Issue Latch")

    # 


def test_decode_end2end():

def main():

if __name__ == "__main__":
    