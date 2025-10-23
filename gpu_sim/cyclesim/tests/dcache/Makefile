# --- Makefile to run GPU simulator tests (Located in tests/dcache/) ---

# Define the Python interpreter
PYTHON = python3.12

# --- Test Script Module Paths (relative to PROJECT_ROOT) ---
TEST_DCACHE_MISS_MODULE = gpu_sim.cyclesim.tests.dcache.readFromAllBanks # Renamed for clarity
TEST_DCACHE_HIT_MODULE = gpu_sim.cyclesim.tests.dcache.readHits

# Define the project root relative to this Makefile's location
PROJECT_ROOT = ../../../../

# --- Log File Names (created in PROJECT_ROOT) ---
LOG_FILE_MISS = readFromAllBanks_log.txt
LOG_FILE_HIT = cache_hit_test_log.txt

# --- Targets ---

# Default target: run both tests
all: test_miss test_hits

# Target to run the L1 dcache miss test (one request per bank)
test_miss:
	@echo "Running L1 dcache miss test (one per bank)..."
	# Change to the project root before running the python module command
	cd $(PROJECT_ROOT) && $(PYTHON) -m $(TEST_DCACHE_MISS_MODULE)
	@echo "L1 dcache miss test finished. Check log file ($(LOG_FILE_MISS) in gpu/)."

# Target to run the L1 dcache hit test (prime then hit)
test_hits:
	@echo "Running L1 dcache hit test (prime then hit)..."
	# Change to the project root before running the python module command
	cd $(PROJECT_ROOT) && $(PYTHON) -m $(TEST_DCACHE_HIT_MODULE)
	@echo "L1 dcache hit test finished. Check log file ($(LOG_FILE_HIT) in gpu/)."

# Target to clean intermediate files and logs
clean:
	@echo "Cleaning up project..."
	# Remove the specific log files from the project root
	rm -f $(PROJECT_ROOT)/$(LOG_FILE_MISS)
	rm -f $(PROJECT_ROOT)/$(LOG_FILE_HIT)
	# Find and remove all __pycache__ directories within the project root
	find $(PROJECT_ROOT) -type d -name "__pycache__" -exec rm -rf {} +
	# Find and remove all .pyc files within the project root
	find $(PROJECT_ROOT) -type f -name "*.pyc" -delete
	@echo "Cleanup complete."

# Phony target ensures targets always run, even if files with the same name exist
.PHONY: all test_miss test_hits clean
