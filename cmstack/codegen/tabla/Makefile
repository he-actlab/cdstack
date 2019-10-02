BENCHMARK := linearR-55
INSTRUCTIONS_PATH := ../fpga/hw-imp/include/instructions/$(BENCHMARK)/compute-inst/

SIMULATOR := ./tabla_cyclesim.py

NUM_PE ?= 56
PES_PER_PU ?= 8
BANDWIDTH ?= 1
PRECISION ?= 2

all:
	@$(SIMULATOR) -num_pe $(NUM_PE) -bin_path $(INSTRUCTIONS_PATH) -pes_per_pu $(PES_PER_PU) -bandwidth $(BANDWIDTH) -precision $(PRECISION) -v
