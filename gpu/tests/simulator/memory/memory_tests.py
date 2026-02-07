import sys
from pathlib import Path

gpu_sim_root = Path(__file__).resolve().parents[3]
sys.path.append(str(gpu_sim_root))

from common.custom_enums_multi import *
from common.custom_enums import Op
from simulator.src.mem.icache_stage import ICacheStage
from simulator.src.mem.icache_stage import ICacheStage
from simulator.src.mem.mem_controller import MemController
from simulator.src.mem.Memory import Mem
from simulator.src.decode.decode_class import DecodeStage
from simulator.base_class import *