# 🧠 SoCET GPU Pipeline Simulation Framework

This repository implements a **modular, cycle-accurate GPU pipeline simulator**.  
It models how instructions flow between stages (e.g., Fetch → Decode → Execute → Writeback) using handshake-based interfaces.  

Each stage operates independently and communicates via the `StageInterface`, making it easy to test, replace, or extend specific stages such as `Decode`, `Execute`, or `Memory`.

---

## 🚀 Quick Overview

Each pipeline stage communicates through a **`StageInterface`** object, which manages:
- **valid/ready handshakes**
- **cycle-based latency**
- **backpressure and stalls**

Each simulation **cycle** runs in three main phases:

1. Every `StageInterface` advances timing (`.tick()`).
2. Each `PipelineStage` executes its `.cycle()`, which:
   - Pulls data from its input interface (`.receive()`).
   - Processes it (`.process()`).
   - Sends results to its output interface (`.send()`).
3. The simulator runs stages **back-to-front** each cycle to avoid overwriting pending values.

---

## 📦 Code Structure

```
SoCET_GPU/
│
├── StageInterface      → handshake and timing between pipeline stages
├── PipelineStage       → base class for functional units
├── DecodeStage         → example: instruction decoder
├── SM                  → Streaming Multiprocessor that connects stages
│
└── test_decode.py      → example standalone testbench
```

---

## 🧩 1. Creating a New Pipeline Stage

Each stage is derived from the `PipelineStage` base class.  
To define your own stage (e.g., **Execute**):

```python
from pipeline import PipelineStage

class ExecuteStage(PipelineStage):
    def __init__(self, parent_core):
        super().__init__("Execute", parent_core)
        self.busy = False

    def process(self, inst):
        # Perform ALU or functional execution.
        if not inst:
            return None

        op = inst.get("decoded_fields", {}).get("mnemonic", "nop")
        if op == "add":
            inst["exec_result"] = "ALU_ADD_COMPLETED"
        elif op == "mul":
            inst["exec_result"] = "ALU_MUL_COMPLETED"
        else:
            inst["exec_result"] = "NOP"

        return inst
```

✅ **Notes**
- `process()` runs once per valid input.
- Return the processed instruction dict.
- Return `None` to stall or skip processing.

---

## 🔌 2. Connecting Stages for Modular Testing

Each stage uses two interfaces: one for input, one for output.  

```python
fetch_decode = StageInterface("IF_FetchDecode", latency=1)
decode_exec  = StageInterface("IF_DecodeExec", latency=1)

decode = DecodeStage("SM_1")
execute = ExecuteStage("SM_1")

decode.connect_output(decode_exec)
execute.connect_input(decode_exec)
```

You can insert additional stages or adjust latency values to simulate pipeline timing and stalls.

---

## 🧠 3. Sending Instructions into the Pipeline

Instructions are represented as Python dictionaries.  
Each must include a `"raw"` key (32-bit integer) representing the encoded instruction.

```python
def make_raw(op7, rd, rs1, mid6):
    return ((mid6 & 0x3F) << 19) | ((rs1 & 0x3F) << 13) | ((rd & 0x3F) << 7) | (op7 & 0x7F)

inst = {"pc": 0x100, "raw": make_raw(0x00, rd=1, rs1=2, mid6=3)}  # ADD
```

To push instructions into the pipeline:

```python
if fetch_decode.can_accept():
    fetch_decode.send(inst)
```

Advance one or more cycles:

```python
for cycle in range(3):
    fetch_decode.tick()
    decode_exec.tick()
    decode.cycle()
    execute.cycle()
```

---

## 🌀 4. Flow of Data and Control

### Handshake Flow Diagram

```
 ┌──────────────────────────────┐
 │          Upstream            │
 │ (e.g., Fetch or Testbench)   │
 └──────────────┬───────────────┘
                │ send()
                ▼
     ┌────────────────────────┐
     │     StageInterface     │
     │ ┌────────────────────┐ │
     │ │ next_data, valid   │ │
     │ │ data, ready flags  │ │
     │ └────────────────────┘ │
     └────────────┬───────────┘
                  │ receive()
                  ▼
          ┌────────────────────┐
          │   PipelineStage    │
          │ (e.g., Decode)     │
          │ process(inst)      │
          └────────────────────┘
                  │ send()
                  ▼
     ┌────────────────────────┐
     │     StageInterface     │
     │ (to next pipeline)     │
     └────────────────────────┘
```

### Cycle-by-Cycle Summary

| Step | Action |
|------|--------|
| 1 | Upstream sends instruction via `.send()` |
| 2 | `.tick()` moves `next_data → data` (latency applied) |
| 3 | Downstream stage retrieves via `.receive()` |
| 4 | `.process()` executes functional logic |
| 5 | `.send()` pushes result to next stage |
| 6 | `.tick()` commits output for next cycle |

---

## ⚙️ 5. Example Decode Test

Below is a minimal testbench to simulate only the **Decode** stage:

```python
test_in = StageInterface("IF_FetchDecode", latency=1)
test_out = StageInterface("IF_DecodeExec", latency=1)
decode = DecodeStage("SM_1")
decode.connect_interfaces(test_in, test_out)

instructions = [
    {"pc": 0x100, "raw": make_raw(0x00, rd=1, rs1=2, mid6=3)},  # ADD
    {"pc": 0x104, "raw": make_raw(0x10, rd=5, rs1=6, mid6=0)},  # ADDI
]

for inst in instructions:
    print(f"\nIssuing instruction PC=0x{inst['pc']:x}")
    while not test_in.can_accept():
        test_in.tick()
        test_out.tick()
        decode.cycle()

    test_in.send(inst)
    for _ in range(2):
        test_in.tick()
        test_out.tick()
        decode.cycle()

    print(f"Output: {test_out.data}")
```

Expected output:

```text
Issuing instruction PC=0x100
Output: {'decoded': True, 'decoded_fields': {'mnemonic': 'add', 'type': 'R', ...}}

Issuing instruction PC=0x104
Output: {'decoded': True, 'decoded_fields': {'mnemonic': 'addi', 'type': 'I', ...}}
```

---

## 🧮 6. Adding Latency or Stalls

Each interface supports latency simulation:

```python
if_decode_exec = StageInterface("IF_DecodeExec", latency=2)
```

This delays data by 2 cycles before the next stage sees it, automatically simulating pipeline timing.

---

## 🧰 7. Extending to a Full Pipeline

To build and simulate a full 4-stage scalar pipeline:

```python
sm = SM()
for cycle in range(20):
    sm.cycle()
    sm.print_pipeline_state()
```

The `SM` class runs all stages (Fetch → Decode → Execute → Writeback)  
**back-to-front** to preserve data integrity and timing.

---

## 🧩 Component Summary

| Component | Role |
|------------|------|
| `StageInterface` | Handles valid/ready handshakes and latency between stages |
| `PipelineStage` | Base class defining per-cycle behavior for a stage |
| `DecodeStage` | Implements a functional instruction decoder |
| `SM` | Streaming Multiprocessor that orders and schedules stages |
| Testbench | Sends synthetic instructions and runs per-cycle simulation |

---

## 🧭 Developer Tips

- Always call `.tick()` once per cycle for **each interface**.
- Always call stage `.cycle()` in **reverse order** (back-to-front).
- Use `.can_accept()` before sending to avoid data loss.
- Use `.print_pipeline_state()` or log interface states for debugging.

---

## 📊 Optional: ASCII Timing Diagram

```
Cycle 0 : [SEND] → next_data set on IF_FetchDecode
Cycle 1 : [TICK] → next_data → data | Decode receives input
Cycle 2 : [PROCESS] → Decode sends to IF_DecodeExec
Cycle 3 : [TICK] → next_data → data | Output valid for Execute
```

---

### 🏁 Summary

This framework provides:
- Modular, testable pipeline stages.
- Cycle-accurate, handshake-driven flow control.
- Extendable structure for GPU/CPU microarchitecture modeling.

It’s ideal for **incremental stage development**, **microarchitectural testing**, or **instruction-level simulation**.

---
