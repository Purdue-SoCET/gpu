import math
from collections import deque
from dataclasses import dataclass
from typing import Optional, Tuple, Any, Dict
from abc import ABC, abstractmethod
import sys # For debug printing to stderr

# --- CONFIGURATION ---
cache_config = {
    "cache_size": 65536,  # 64 Kilobytes
    "block_size": 128,     # Size of a cache block in bytes
    "associativity": 8,    # Number of ways per set
    "num_banks": 32,       # Number of cache banks
    "mshr_size": 16        # Number of MSHR queue entries PER BANK
}

# --- DATA CLASSES ---
@dataclass
class MemoryRequest:
    uuid: int
    warp_id: int
    thread_id: int
    address: int
    ldMode: bool
    write_data: Optional[int] = None # Assuming byte write for simplicity

class CacheLine:
    def __init__(self, block_size):
        self.is_valid = False
        self.is_dirty = False
        self.tag = None
        self.data = bytearray(block_size)
        self.lru_counter = 0

class MSHREntry:
    def __init__(self, request: MemoryRequest, block_address: int):
        self.is_valid = True
        self.block_address = block_address
        self.requestor_uuids = {request.uuid} # Use a set for UUIDs
        self.first_request_details: MemoryRequest = request
        self.countdown = 200

# --- FUNCTIONAL UNIT PARENT CLASS ---
class FunctionalUnit(ABC):
    def __init__(self, name: str): self.name = name
    @abstractmethod
    def cycle(self): pass

# --- L1 DATA CACHE IMPLEMENTATION ---

class L1DataCache(FunctionalUnit):

    def __init__(self, cache_config, main_memory: Dict[int, bytearray]):
        super().__init__(name="L1_DCache")
        # --- Store Configuration ---
        self.cache_size = cache_config['cache_size']
        self.block_size = cache_config['block_size']
        self.associativity = cache_config['associativity']
        self.num_banks = cache_config['num_banks']
        self.mshr_size = cache_config['mshr_size']

        # --- Define Pipeline Latencies ---
        self.HIT_LATENCY = 1 # Treat hit as resolvable within the cycle it's checked

        # --- Calculate Address Bits --- (Same as before)
        self.block_offset_bits = int(math.log2(self.block_size))
        total_sets = self.cache_size // (self.block_size * self.associativity)
        if total_sets == 0: raise ValueError("Cache size too small for block size and associativity.")
        self.num_sets_per_bank = total_sets // self.num_banks
        if self.num_sets_per_bank == 0: raise ValueError("Cache config results in 0 sets per bank.")
        if total_sets % self.num_banks != 0: raise ValueError("Total sets must be divisible by the number of banks")
        self.bank_bits = int(math.log2(self.num_banks))
        self.set_bits = int(math.log2(self.num_sets_per_bank))
        self.global_lru_clock = 0
        # --- Create Storage --- (Same as before)
        self.banks = [[ [CacheLine(self.block_size) for _ in range(self.associativity)] for _ in range(self.num_sets_per_bank)] for _ in range(self.num_banks)]
        # --- Miss Handling --- (Same as before)
        self.mshr_queues = [deque() for _ in range(self.num_banks)]
        self.active_misses = [None] * self.num_banks
        self.pending_miss_details: Dict[int, MemoryRequest] = {}
        # --- Input/Output Queues --- (Same as before)
        self.request_queue = deque()
        self.response_queue = deque()
        self.miss_notification_queue = deque()

        # --- FIX: ADD THIS LINE BACK ---
        # Store reference to mock main memory
        self.main_memory = main_memory


    # --- Static Helper for Address Parsing --- (Same as before)
    @staticmethod
    def _static_parse_address(address: int, config: dict) -> Tuple[int, int, int, int, int]:
        # (Implementation remains the same)
        block_size = config['block_size']; num_banks = config['num_banks']; cache_size = config['cache_size']; associativity = config['associativity']
        if block_size==0 or associativity==0 or num_banks==0: return 0,0,0,0,0
        block_offset_bits = int(math.log2(block_size))
        total_sets = cache_size // (block_size * associativity)
        if total_sets == 0: return 0,0,0,0,0
        num_sets_per_bank = total_sets // num_banks
        if num_sets_per_bank == 0: return 0,0,0,0,0
        bank_bits = int(math.log2(num_banks))
        set_bits = int(math.log2(num_sets_per_bank))
        address &= 0xFFFFFFFF
        block_offset = address & ((1 << block_offset_bits) - 1)
        block_address_aligned = (address >> block_offset_bits)
        temp_block_addr = block_address_aligned
        bank_index = temp_block_addr & ((1 << bank_bits) - 1)
        temp_block_addr >>= bank_bits
        set_index = temp_block_addr & ((1 << set_bits) - 1)
        temp_block_addr >>= set_bits
        tag = temp_block_addr
        return tag, bank_index, set_index, block_address_aligned, block_offset

    # --- Instance Helper Methods ---
    def _parse_address(self, address: int) -> Tuple[int, int, int, int, int]:
        # (Implementation remains the same)
        return L1DataCache._static_parse_address(address, {
            "block_size": self.block_size, "num_banks": self.num_banks,
            "cache_size": self.cache_size, "associativity": self.associativity
        })

    def _find_in_cache(self, bank_index, set_index, tag) -> Tuple[bool, Optional[int]]:
        # (Implementation remains the same)
        if bank_index >= self.num_banks or set_index >= self.num_sets_per_bank: return False, None
        target_set = self.banks[bank_index][set_index]
        for way_index in range(self.associativity):
            line = target_set[way_index]
            if line.is_valid and line.tag == tag:
                self._update_lru(bank_index, set_index, way_index)
                return True, way_index
        return False, None

    def _find_lru_way(self, bank_index, set_index) -> int:
        # (Implementation remains the same)
        if bank_index >= self.num_banks or set_index >= self.num_sets_per_bank: return 0
        target_set = self.banks[bank_index][set_index]
        lru_way = 0; min_lru_val = float('inf')
        for way_index in range(self.associativity):
            if not target_set[way_index].is_valid:
                # print(f"    [Eviction] Found invalid way {way_index} for bank {bank_index}, set {set_index}.", file=sys.stderr)
                return way_index
        for way_index in range(self.associativity):
            if target_set[way_index].lru_counter < min_lru_val:
                min_lru_val = target_set[way_index].lru_counter
                lru_way = way_index
        print(f"    [Eviction] Found LRU way {lru_way} (count={min_lru_val}) for bank {bank_index}, set {set_index}.", file=sys.stderr)
        return lru_way

    def _update_lru(self, bank_index, set_index, hit_way):
        # (Implementation remains the same)
        if bank_index >= self.num_banks or set_index >= self.num_sets_per_bank or hit_way >= self.associativity: return
        self.global_lru_clock += 1
        self.banks[bank_index][set_index][hit_way].lru_counter = self.global_lru_clock

    # --- _fill_cache_line remains the same ---
    def _fill_cache_line(self, bank_idx, mshr_entry: MSHREntry):
        # (Implementation remains the same)
        temp_address = mshr_entry.block_address << self.block_offset_bits
        tag, _, set_idx, _, _ = self._parse_address(temp_address)
        if bank_idx >= self.num_banks or set_idx >= self.num_sets_per_bank:
             print(f"    ERROR: Invalid bank/set index for fill: bank={bank_idx}, set={set_idx}", file=sys.stderr); return
        victim_way = self._find_lru_way(bank_idx, set_idx)
        line_to_replace = self.banks[bank_idx][set_idx][victim_way]
        if line_to_replace.is_valid and line_to_replace.is_dirty:
            print(f"    [Eviction] WARNING: Dirty victim line! Tag=0x{line_to_replace.tag:X}. (WB not impl.)")
        fetched_data = self.main_memory.get(mshr_entry.block_address)
        if fetched_data is None:
            print(f"    [Fill] ERROR: Block 0x{mshr_entry.block_address:X} not in mock_memory!", file=sys.stderr)
            fetched_data = bytearray(self.block_size)
        elif len(fetched_data) != self.block_size:
            print(f"    [Fill] ERROR: Mock memory data size mismatch for 0x{mshr_entry.block_address:X}!", file=sys.stderr)
            fetched_data = bytearray(self.block_size)
        else:
             fetched_data = bytearray(fetched_data)
             # print(f"    [Fill] Fetched {self.block_size} bytes for block 0x{mshr_entry.block_address:X}.", file=sys.stderr)
             # print(f"      Data sample (first 8 bytes): {bytes(fetched_data[:8]).hex()}", file=sys.stderr) # Debug print
        line_to_replace.is_valid = True
        line_to_replace.tag = tag
        line_to_replace.data = fetched_data
        first_request = mshr_entry.first_request_details
        if first_request.ldMode:
             offset = self._parse_address(first_request.address)[4]
             if isinstance(first_request.write_data, int):
                 if 0 <= offset < self.block_size:
                      line_to_replace.data[offset] = first_request.write_data & 0xFF
                      print(f"    [Fill] Merged write 0x{first_request.write_data:X} at offset {offset}", file=sys.stderr)
                      line_to_replace.is_dirty = True
                 else: print(f"    [Fill] ERROR: Invalid offset {offset} for merge.", file=sys.stderr); line_to_replace.is_dirty = False
             else: print(f"    [Fill] WARNING: Write miss MSHR no data.", file=sys.stderr); line_to_replace.is_dirty = False
        else: line_to_replace.is_dirty = False
        self._update_lru(bank_idx, set_idx, victim_way)


    # --- _process_hit remains the same ---
    def _process_hit(self, bank_idx, set_idx, way_idx, request: MemoryRequest):
        # (Implementation remains the same as previous response, uses offset)
        if bank_idx >= self.num_banks or set_idx >= self.num_sets_per_bank or way_idx >= self.associativity: return None
        line = self.banks[bank_idx][set_idx][way_idx]
        response_data = None
        tag, _, _, _, offset = self._parse_address(request.address)
        word_offset = offset & ~0x3
        byte_offset_in_word = offset & 0x3
        if request.ldMode: # Write
            if isinstance(request.write_data, int):
                if 0 <= offset < self.block_size:
                    line.data[offset] = request.write_data & 0xFF
                    line.is_dirty = True
                    print(f"    -> Write HIT (Byte) at bank {bank_idx}, set {set_idx}, way {way_idx}, offset {offset}", file=sys.stderr)
                else: print(f"    ERROR: Invalid offset {offset} for write hit.", file=sys.stderr)
            else: print(f"    WARNING: Write hit request has no write_data.", file=sys.stderr)
        else: # Read
            if 0 <= word_offset < self.block_size:
                word_bytes = line.data[word_offset : word_offset + 4]
                if len(word_bytes) == 4:
                     response_data = int.from_bytes(word_bytes, byteorder='little')
                     print(f"    -> Read HIT (Word) at bank {bank_idx}, set {set_idx}, way {way_idx}, word_offset {word_offset}, Data=0x{response_data:X}", file=sys.stderr)
                else: print(f"    ERROR: Could not read full word at offset {word_offset}.", file=sys.stderr); response_data = 0
            else: print(f"    ERROR: Invalid word offset {word_offset} for read hit.", file=sys.stderr); response_data = 0
        self._update_lru(bank_idx, set_idx, way_idx)
        return response_data

    # --- THE MODIFIED CYCLE METHOD --- (Remains the same as 1-cycle hit version)
    def cycle(self):
        # (Implementation remains the same)
        print(f"--- Cycle {self.name} ---", file=sys.stderr) # Use stderr for logs
        # --- 1. Handle Active Misses ---
        for bank_idx in range(self.num_banks):
            active_miss = self.active_misses[bank_idx]
            if active_miss is not None:
                active_miss.countdown -= 1
                # print(f"  [Bank {bank_idx}] Active miss block 0x{active_miss.block_address:X}, countdown: {active_miss.countdown}", file=sys.stderr)
                if active_miss.countdown == 0:
                    print(f"  [Bank {bank_idx}] MISS COMPLETE for block 0x{active_miss.block_address:X}", file=sys.stderr)
                    self._fill_cache_line(bank_idx, active_miss)
                    _, fill_bank_idx, fill_set_idx, _, _ = self._parse_address(active_miss.block_address << self.block_offset_bits)
                    filled_way = -1; tag_to_find = self._parse_address(active_miss.block_address << self.block_offset_bits)[0]
                    for w in range(self.associativity):
                         line = self.banks[bank_idx][fill_set_idx][w]
                         if line.is_valid and line.tag == tag_to_find: filled_way = w; break
                    for uuid in active_miss.requestor_uuids:
                        original_request = self.pending_miss_details.get(uuid)
                        response_word = 0
                        if original_request is None: print(f"    ERROR: No details for UUID {uuid}", file=sys.stderr)
                        elif filled_way == -1: print(f"    ERROR: Cannot find filled line for UUID {uuid}", file=sys.stderr)
                        else:
                             _, _, _, _, original_offset = self._parse_address(original_request.address)
                             word_offset = original_offset & ~0x3
                             filled_line = self.banks[bank_idx][fill_set_idx][filled_way]
                             if 0 <= word_offset < self.block_size:
                                  word_bytes = filled_line.data[word_offset : word_offset + 4]
                                  if len(word_bytes) == 4:
                                       response_word = int.from_bytes(word_bytes, byteorder='little')
                                       # print(f"    -> Extracted word 0x{response_word:X} at offset {word_offset} for UUID {uuid}", file=sys.stderr) # Less verbose
                                  else: print(f"    ERROR: Cannot read word after fill for UUID {uuid}", file=sys.stderr)
                             else: print(f"    ERROR: Invalid word offset {word_offset} after fill for UUID {uuid}", file=sys.stderr)
                        response = {"uuid": uuid, "data": response_word}
                        self.response_queue.append(response)
                        print(f"    -> Sent data word to response_queue for UUID {uuid}", file=sys.stderr)
                        if uuid in self.pending_miss_details: del self.pending_miss_details[uuid]
                    self.active_misses[bank_idx] = None
        # --- Stage 2 Removed (No hit pipeline) ---
        # --- 3. Launch New Misses ---
        for bank_idx in range(self.num_banks):
            if self.active_misses[bank_idx] is None and self.mshr_queues[bank_idx]:
                oldest_miss = self.mshr_queues[bank_idx].popleft()
                self.active_misses[bank_idx] = oldest_miss
                print(f"  [Bank {bank_idx}] LAUNCHING miss fetch for block 0x{oldest_miss.block_address:X} (UUID {list(oldest_miss.requestor_uuids)[0]}). 200-cycle timer started.", file=sys.stderr)
        # --- 4. Process New Requests ---
        if self.request_queue:
            request = self.request_queue[0] # Peek
            # print(f"  [New Request] Processing request for Addr 0x{request.address:X} (UUID: {request.uuid}, {'Write' if request.ldMode else 'Read'})", file=sys.stderr) # Less verbose
            tag, bank_idx, set_idx, block_addr, offset = self._parse_address(request.address)
            if bank_idx >= self.num_banks or set_idx >= self.num_sets_per_bank:
                print(f"    ERROR: Invalid address mapping. Bank={bank_idx}, Set={set_idx}. Discarding request.", file=sys.stderr)
                self.request_queue.popleft(); return
            is_hit, hit_way = self._find_in_cache(bank_idx, set_idx, tag)
            if is_hit:
                self.request_queue.popleft()
                response_data = self._process_hit(bank_idx, set_idx, hit_way, request)
                response = {"uuid": request.uuid, "data": response_data}
                self.response_queue.append(response) # Send immediately for 1-cycle hit
                # print(f"  [Hit Pipeline] HIT processed for UUID {request.uuid}. Sent data word to response_queue in SAME cycle.", file=sys.stderr) # Less verbose
            else: # Miss
                # print(f"    -> CACHE MISS (Block 0x{block_addr:X}).", file=sys.stderr) # Less verbose
                is_secondary = False; active_miss = self.active_misses[bank_idx]
                if active_miss and active_miss.block_address == block_addr:
                    active_miss.requestor_uuids.add(request.uuid)
                    is_secondary = True
                    # print(f"    -> Secondary miss (merged with active request).", file=sys.stderr)
                else:
                    for entry in self.mshr_queues[bank_idx]:
                        if entry.block_address == block_addr:
                            entry.requestor_uuids.add(request.uuid)
                            is_secondary = True
                            # print(f"    -> Secondary miss (merged with queued request).", file=sys.stderr)
                            break
                if is_secondary:
                    self.request_queue.popleft()
                    self.pending_miss_details[request.uuid] = request
                    self.miss_notification_queue.append(request)
                    print(f"    -> Sent miss notification for secondary miss UUID {request.uuid}.", file=sys.stderr)
                elif len(self.mshr_queues[bank_idx]) < self.mshr_size:
                    self.request_queue.popleft()
                    new_mshr = MSHREntry(request, block_addr)
                    self.mshr_queues[bank_idx].append(new_mshr)
                    self.pending_miss_details[request.uuid] = request
                    self.miss_notification_queue.append(request)
                    print(f"    -> Primary miss. Added to MSHR queue for bank {bank_idx}.", file=sys.stderr)
                    print(f"    -> Sent miss notification for primary miss UUID {request.uuid}.", file=sys.stderr)
                else: # Stall
                    print(f"    -> STALL! MSHR queue for bank {bank_idx} is full.", file=sys.stderr)
                    pass
        # else: print("  [New Request] No new requests this cycle.", file=sys.stderr)

    # --- Public method for LSU ---
    def accept_request(self, request: MemoryRequest):
         """Adds a new memory request to the input queue."""
         # print(f"[Input] Accepted request for Addr 0x{request.address:X} (UUID: {request.uuid})", file=sys.stderr) # Less verbose
         self.request_queue.append(request)

