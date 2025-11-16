# decode_test.py — Comprehensive & diagnostic tests for DecodeStage

import sys
from pathlib import Path
parent = Path(__file__).resolve().parent.parent
sys.path.append(str(parent))

from base import LatchIF, ForwardingIF, Instruction

from units.icache import ICacheStage
from bitstring import Bits
