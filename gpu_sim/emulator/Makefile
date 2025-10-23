PYTHON := venv/bin/python3
EMULATOR := src/emulator.py
INPUT_FILE := meminit.hex
BLOCK_DIM := 4 4 2
START_PC := 0

run:
	$(PYTHON) $(EMULATOR) $(INPUT_FILE) $(BLOCK_DIM) $(START_PC)

clean:
	rm -f *.out *.log