#!/usr/bin/env python3
import json
help_message = """
Instruction Format

<Function Type >
< DEST0 N ID > < DEST0 INDEX >
< DEST1 N ID > < DEST1 INDEX >
< DEST2 N ID > < DEST2 INDEX >
< SRC0 N ID > < SRC0 INDEX >
< SRC1 N ID > < SRC1 INDEX >
< SRC2 N ID > < SRC2 INDEX >

------------------------------
<Function Type> can be of the type:
FN_PASS : 0
FN_ADD : 1
FN_SUB : 2
FN_MUL : 3
FN_MAC ; 4
FN_DIV : 5
FN_SQR : 6
FN_SIG : 7
FN_GAU : 8

------------------------------
<N ID> is Namespace ID. It can be of the type:
NAMESPACE_NULL : 0
NAMESPACE_WEIGHT : 1
NAMESPACE_DATA : 2
NAMESPACE_GRADIENT : 3
NAMESPACE_INTERIM : 4
NAMESPACE_META : 5
NAMESPACE_NEIGHBOR : 6    # [0] = PE_NEIGHBOR, [1] = PU_NEIGHBOR
NAMESPACE_BUS : 7    # [0] = PE_BUS, [1] = PU_BUS

------------------------------
<INDEX> means different things:
When N ID is weight, data, gradient, meta, interim: INDEX is the actual index in the namespace
When N ID is neighbor: INDEX [0] is neighboring PE id, or INDEX [1] is neighboring PU id
When N ID is bus: INDEX [0] is PE id using the pe bus, or INDEX [1] is PU id and PE id

"""
import argparse
import bisect
from math import ceil

class tabla_pe:
    id = None
    pu = None
    stall = False
    write_stall = False
    interim_stall = False
    stall_code = ""

    # Instruction Queue
    instruction_queue = []

    # 5 stage pipeline
    stage_fetch = None
    stage_decode = None
    stage_data_read = None
    stage_execute = None
    stage_data_write = None

    # Interconnect
    pe_neighbor_reg = None
    pu_neighbor_reg = None
    pe_bus_reg = None
    global_bus_reg = None

    prev_pe = None
    next_pe = None

    prev_pu = None
    next_pu = None

    def __init__(self, id, pu):
        self.id = id
        self.pu = pu
        self.stall = False
        self.interim_stall = False
        self.stall_code = ""
        self.instruction_queue = []

        self.stage_fetch = None
        self.stage_decode = None
        self.stage_data_read = None
        self.stage_execute = None
        self.stage_data_write = None

        self.pe_neighbor_reg = None
        self.pu_neighbor_reg = None
        self.pe_bus_reg = None
        self.global_bus_reg = None

        self.prev_pe = None
        self.next_pe = None

        self.prev_pu = None
        self.next_pu = None

    def __str__ (self):
        ret = ""
        #  ret +=  "PE{0} PU{1}\nStall = {2}".format(self.id, self.pu, self.stall)
        #  ret += "\nInstructions Left : {0}".format(self.get_num_instructions())
        #  ret += "\nStage Fetch       : {0}".format(self.stage_fetch)
        #  ret += "\nStage Decode      : {0}".format(self.stage_decode)
        #  ret += "\nStage Data Read   : {0}".format(self.stage_data_read)
        #  ret += "\nStage Compute     : {0}".format(self.stage_execute)
        #  ret += "\nStage Data Write  : {0}".format(self.stage_data_read)
        #if not self.stall and self.stage_execute is not None:
        if self.stage_execute is not None:
            ret += "PE{0} PU{1}: {2}: Stalled={3}\t{4}".format(str(self.id).ljust(5), str(self.pu).ljust(5), str(self.stage_execute).ljust(80), self.stall, self.stall_code)
            if self.pe_neighbor_reg is not None:
                ret += " NN_reg " + str(self.pe_neighbor_reg)
        #ret += "\nStage Write Back  : {0}".format(self.stage_data_write)
        #if (self.pe_bus_reg is not None):
            #ret += "\nPE Bus Reg        : {0}".format(self.pe_bus_reg)
        return ret

    def add_instruction (self, inst):
        self.instruction_queue.append(inst)

    def get_num_instructions (self):
        return len(self.instruction_queue)

    def fetch (self):
        if self.get_num_instructions() > 0 and not self.stall:
            self.stage_fetch = self.instruction_queue[0]
            del (self.instruction_queue[0])
        elif not self.stall:
            self.stage_fetch = None

    def decode (self):

        if self.stage_fetch is None and not self.stall:
            self.stage_decode = None
            return
        elif self.stall:
            return

        operation_bitwidth = 3
        namespace_bitwidth = 3
        index_bitwidth = 8

        op_bits = self.stage_fetch[:operation_bitwidth]
        dests = []
        srcs = []

        op = int(op_bits, 2)

        start_point = operation_bitwidth

        for i in range(3):
            ns_bits = self.stage_fetch[start_point:start_point + namespace_bitwidth]
            namespace = int(ns_bits, 2)
            index_bits = self.stage_fetch[start_point + namespace_bitwidth:start_point + namespace_bitwidth + index_bitwidth]
            index = int(index_bits, 2)
            dst = {
                "namespace": namespace,
                "index": index
            }
            dests.append(dst)
            start_point += (namespace_bitwidth + index_bitwidth)
        for i in range(3):
            ns_bits = self.stage_fetch[start_point:start_point + namespace_bitwidth]
            ns = int(ns_bits, 2)
            index_bits = self.stage_fetch[start_point + namespace_bitwidth:start_point + namespace_bitwidth + index_bitwidth]
            index = int(index_bits, 2)
            src = {
                "namespace": ns,
                "index": index
            }
            srcs.append(src)
            start_point += (namespace_bitwidth + index_bitwidth)
        inst = pe_instruction(srcs, dests, op, self.id, self.prev_pe, self.next_pe, self.prev_pu, self.next_pu)
        #print (inst)
        self.stage_decode = inst

    def data_write(self, pe_neighbor_bus, pe_bus, global_bus, pu_neighbor_bus):
        #if self.interim_stall:
        #    self.stage_data_write = None
        #    self.interim_stall = False
        #elif not self.stall:
        #    self.stage_data_write = self.stage_execute
        #else:
        #    self.stage_data_write = None

        if self.stall and not self.write_stall:
            self.stage_data_write = None
        else:
            self.stage_data_write = self.stage_execute

        self.stall = False
        self.stall_code = ""

        # Write Stall logic
        if self.stage_data_write is not None and not self.stall:
            dst = self.stage_data_write.dst
            for d in dst:
                if d["namespace"] is 6:
                    pe_pu_bus_switch = d["index"] % 2
                    if pe_pu_bus_switch is 0 and self.prev_pe is not None:
                        pe_neighbor_bus.append({"src":self.id, "dst":self.prev_pe.id})
                    elif self.pu > 0:
                        destination_pu = self.prev_pu
                        source_pu = self.pu
                        pu_neighbor_bus[self.pu-1] = {"src":self.pu, "dst":destination_pu}
                elif d["namespace"] is 7:
                    # Bus Transaction required
                    pe_pu_bus_switch = d["index"] % 2
                    if pe_pu_bus_switch is 0:
                        if pe_bus[self.pu] is None:
                            destination = d["index"] >> 1
                            source = self.id
                            pe_bus[self.pu] = {"src":source, "dst":destination}
                        else:
                            self.stall = True
                            self.stall_code += "Waiting for PE bus data for Write"
                    else:
                        if global_bus[0] is None:
                            destination_pu = d["index"] >> 1
                            source_pu = self.pu
                            global_bus[0] = {"src":source_pu, "dst":destination_pu}
                        else:
                            self.stall = True
                            self.stall_code += "Waiting for PU bus data for Write"

        self.write_stall = self.stall


    def execute(self, pe_neighbor_bus, pe_bus, global_bus, pu_neighbor_bus):

        if not self.stall:
            self.stage_execute = self.stage_data_read

        # Read Stall logic
        if self.stage_execute is not None and not self.stall:
            src = self.stage_execute.src
            for s in src:
                if s["namespace"] is 6:
                    pe_pu_bus_switch = s["index"] % 2
                    if pe_pu_bus_switch is 0:
                        if self.pe_neighbor_reg is None:
                            self.stall = True
                            self.stall_code += "Waiting for PE neighbor data"
                    elif pe_pu_bus_switch is 1:
                        if self.pu_neighbor_reg is None:
                            self.stall = True
                            self.stall_code += "Waiting for PU neighbor data"
                elif s["namespace"] is 7:
                    # Bus Transaction required
                    pe_pu_bus_switch = s["index"] % 2
                    if pe_pu_bus_switch is 0:
                        if self.pe_bus_reg is None:
                            self.stall = True
                            self.stall_code += "Waiting for PE bus data"
                    else:
                        if self.global_bus_reg is None:
                            self.stall = True
                            self.stall_code += "Waiting for PU bus data"

        # Interim Read Stall logic
        if self.stage_execute is not None and not self.stall and self.stage_data_write is not None:
            src = self.stage_execute.src
            for s in src:
                if s["namespace"] is 4:
                    source_index = s["index"]
                    for d in self.stage_data_write.dst:
                        destination_index = d["index"]
                        if destination_index is source_index and d["namespace"] is 4:
                            #print (self.stage_data_write, d)
                            self.stall = True
                            self.interim_stall = True
                    if self.stall:
                        self.stall_code += "Waiting for Interim write"

        # Update registers
        if not self.stall and self.stage_execute is not None:
            src = self.stage_execute.src
            for s in src:
                if s["namespace"] is 6:
                    pe_pu_bus_switch = s["index"] % 2
                    if pe_pu_bus_switch is 0:
                        self.pe_neighbor_reg = None
                    elif pe_pu_bus_switch is 1:
                        self.pu_neighbor_reg = None
                elif s["namespace"] is 7:
                    # Bus Transaction required
                    pe_pu_bus_switch = s["index"] % 2
                    if pe_pu_bus_switch is 0:
                        self.pe_bus_reg = None
                    else:
                        self.global_bus_reg = None



    def data_read(self):
        if not self.stall:
            self.stage_data_read = self.stage_decode


class pe_instruction:
    src = None
    dst = None
    op = None
    pe_id = None
    pu_id = None
    prev_pe = None
    next_pe = None
    prev_pu = None
    next_pu = None

    def __init__(self, src, dst, op, pe_id, prev_pe, next_pe, prev_pu, next_pu):
        self.src = src
        self.dst = dst
        self.op  = op
        self.pe_id = pe_id
        self.pu_id = int(pe_id/8)
        self.prev_pe = prev_pe
        self.next_pe = next_pe
        self.prev_pu = prev_pu
        self.next_pu = next_pu

    def __str__(self):
        string_op = self.op_str(self.op)
        if (string_op is "Pass"):
            return "{0}, {1}, {2} = ".format(
                self.namespace_str(self.dst[0]),
                self.namespace_str(self.dst[1]),
                self.namespace_str(self.dst[2])) + \
                   "{0} , {1}".format(
                       self.namespace_str(self.src[0], "source"),
                       self.namespace_str(self.src[1], "source"))
        elif (string_op is "Add"):
            return "{0}, {1}, {2} = ".format(
                       self.namespace_str(self.dst[0]),
                       self.namespace_str(self.dst[1]),
                       self.namespace_str(self.dst[2])) + \
                   "{0} + {1}".format(
                       self.namespace_str(self.src[0], "source"),
                       self.namespace_str(self.src[1], "source"))
        elif (string_op is "Subtract"):
            return "{0}, {1}, {2} = ".format(
                self.namespace_str(self.dst[0]),
                self.namespace_str(self.dst[1]),
                self.namespace_str(self.dst[2])) + \
                   "{0} - {1}".format(
                       self.namespace_str(self.src[0], "source"),
                       self.namespace_str(self.src[1], "source"))
        elif (string_op is "Multiply"):
            return "{0}, {1}, {2} = ".format(
                self.namespace_str(self.dst[0]),
                self.namespace_str(self.dst[1]),
                self.namespace_str(self.dst[2])) + \
                   "{0} * {1}".format(
                       self.namespace_str(self.src[0], "source"),
                       self.namespace_str(self.src[1], "source"))
        else:
            print ("error" + string_op)
            exit(-1)
            return "ERROR"

    def op_str(self, op):
        op_dict = {0: "Pass",
                   1: "Add",
                   2: "Subtract",
                   3: "Multiply",
                   4: "Communicate",
                   5: "Divide",
                   6: "Square",
                   7: "Sigmoid",
                   8: "Gaussian"}
        return op_dict[op]

    def namespace_str (self, dst, type="destination"):
        ret = ""
        dst_dict = {0: "Null",
                   1: "Weight",
                   2: "Data",
                   3: "Gradient",
                   4: "Interim",
                   5: "Meta",
                   6: "Neighbor",
                   7: "Bus"}
        if (dst["namespace"] is 0):
            ret = "-"
        if (dst["namespace"] < 6):
            ret = "{0}[{1}]".format(dst_dict[dst["namespace"]], str(dst["index"]))
        elif (dst["namespace"] is 6):
            pe_pu_switch = dst["index"] % 2
            if (pe_pu_switch is 0):
                if type is "source":
                    ret = "PE_neighbor[PE{0}]".format(self.next_pe.id)
                else:
                    ret = "PE_neighbor[PE{0}]".format(self.prev_pe.id)
            else:
                if type is "source":
                    ret = "PU_neighbor[PU{0}]".format(self.next_pu)
                else:
                    ret = "PU_neighbor[PU{0}]".format(self.prev_pu)
        else:
            pe_pu_switch = dst["index"] % 2
            if (pe_pu_switch is 0):
                ret = "PE_bus[{0}]".format(str(dst["index"] >> 1))
            else:
                ret = "PU_bus[{0}]".format(str(dst["index"] >> 1))

        return ret.ljust(20)

    def get_sources (self):
        None


class tabla_simulator:
    pe = []
    cycle_count = None
    num_pu = None

    pe_bus = []
    pe_neighbor_bus = []
    global_bus = []
    pu_neighbor_bus = []

    verbosity = False

    bin_path = None
    bandwidth = None
    precision = None

    def __init__(self, config_path,bin_path, bandwidth, precision, v):
        self.read_config(config_path)
        self.cycle_count = 0
        self.num_pu = int(ceil(self.num_pes / self.pes_per_pu))
        if self.verbosity:
            print ("Initializing Tabla with {0} PEs and {1} PUs".format(self.num_pes, self.num_pu))
        for i in range(self.num_pu):
            self.pe_bus.append(None)
        self.global_bus = [None]
        for i in range(self.num_pu-1):
            self.pu_neighbor_bus.append(None)
        self.bin_path = bin_path
        self.bandwidth = bandwidth
        self.precision = precision
        self.verbosity = v

        self.load_instructions(bin_path)
        self.connect_pes()

    def load_instructions(self, inst_path):
        if self.verbosity:
            print ("Loading instructions from path: {0}".format(inst_path))
        for n in range(self.num_pes):
            pu_id = int(n/self.pes_per_pu)
            p = tabla_pe(n, pu_id)
            pe_binary = inst_path + "/pe{0}.txt".format(str(n).zfill(2))
            with open(pe_binary, 'r') as f:
                for line in f:
                    raw_instruction = line.rstrip()
                    if raw_instruction is not '0':
                        p.add_instruction (raw_instruction)
            self.pe.append(p)

    def connect_pes(self):
        for n in range(self.num_pes):
            p = self.pe[n]
            if (n % self.pes_per_pu) is not 0:
                p.prev_pe = self.pe[n-1]
                p.prev_pe.next_pe = p
            elif n is not self.pes_per_pu*int((self.num_pes-1)/self.pes_per_pu):
                p.prev_pe = self.pe[n + self.pes_per_pu - 1]
                p.prev_pe.next_pe = p
            else:
                p.prev_pe = self.pe[-1]
                p.prev_pe.next_pe = p

        for n in range(self.num_pu):
            p = self.pe[n*self.pes_per_pu]
            if n is 0:
                p.prev_pu = self.num_pu-1
                p.next_pu = n + 1
            elif n > 0 and n is not self.num_pu - 1:
                p.prev_pu = n - 1
                p.next_pu = n + 1
            else:
                p.prev_pu = n - 1
                p.next_pu = 0

    def simulate(self):
        instructions_remaining = 0
        for p in self.pe:
            instructions_remaining = max(instructions_remaining, p.get_num_instructions())

        if self.verbosity:
            print ("Simulation begin")
        while (self.execute_step()):
            None

        if self.verbosity:
            print ("Compute Cycles = {0}".format(self.cycle_count))

        return self.cycle_count

    def execute_step(self):
        if self.verbosity:
            print ("*"*50)
            print ("Cycle {0}".format(self.cycle_count))
            print ("*"*50)

        # data write
        for p in self.pe:
            p.data_write(self.pe_neighbor_bus, self.pe_bus, self.global_bus, self.pu_neighbor_bus)

        # compute
        for p in self.pe:
            p.execute(self.pe_neighbor_bus, self.pe_bus, self.global_bus, self.pu_neighbor_bus)


        # data read
        for p in self.pe:
            p.data_read()
        # decode
        for p in self.pe:
            p.decode()

        # fetch
        for p in self.pe:
            p.fetch()

        instructions_remaining = False
        for n in range(self.num_pes):
            p = self.pe[n]
            pe_instructions_remaining = (p.get_num_instructions() > 0) or \
                                        (p.stage_fetch is not None) or \
                                        (p.stage_decode is not None) or \
                                        (p.stage_data_read is not None) or \
                                        (p.stage_execute is not None) or \
                                        (p.stage_data_write is not None)
            instructions_remaining = instructions_remaining or pe_instructions_remaining

        for n in self.pe_neighbor_bus:
            dst_pe = n["dst"]
            self.pe[dst_pe].pe_neighbor_reg = n

        for pu in range(self.num_pu):
            if self.verbosity:
                print ("PU{0} - PE Bus status = {1}".format(pu, self.pe_bus[pu]))
            if self.pe_bus[pu] is not None:
                dst = self.pe_bus[pu]["dst"]
                self.pe[dst].pe_bus_reg = self.pe_bus[pu]
                self.pe_bus[pu] = None

        for pu in range(self.num_pu-1):
            if self.verbosity:
                print ("PU{0} - PU Bus status = {1}".format(pu, self.pu_neighbor_bus[pu]))
            if self.pu_neighbor_bus[pu] is not None:
                dst_pu = self.pu_neighbor_bus[pu]["dst"]
                dst_pe = dst_pu*self.pes_per_pu
                self.pe[dst_pe].pu_neighbor_reg = self.pu_neighbor_bus[pu]
                self.pu_neighbor_bus[pu] = None

        for gb in self.global_bus:
            if self.verbosity:
                print ("Tabla - Global Bus status = {0}".format(gb))
            if gb is not None:
                dst_pu = gb["dst"]
                dst_pe = dst_pu*self.pes_per_pu
                self.pe[dst_pe].global_bus_reg = gb
                self.global_bus[0] = None




        if self.verbosity:
            for p in self.pe:
                s = str(p)
                if s is not "":
                    print (s)


        self.cycle_count = self.cycle_count + 1

        if self.verbosity:
            print ("*"*50)
        return instructions_remaining

    def read_config(self, path):
        print("reading config file...", end='')
        with open(path, 'r') as f:
            config = f.read()
        f.close()
        config = json.loads(config)
        self.num_pes = config["num_pes"]
        self.pes_per_pu = config["pes_per_pu"]
        self.ns_size = config["namespace_size"]
        self.ns_int_size = config["namespace_interim_size"]
        self.op_bit = config["op_bit"]
        self.ns_bit = config["ns_bit"]
        self.index_bit = config["index_bit"]
        self.nn_nb_bit = config["nn_nb_bit"]

        print("done")



if __name__ == '__main__':
    bin_path = "./bin"
    prompt = ">> "
    config_path = "./config.json"
    bandwidth = 1
    precision = 2
    verbosity = False

    t = tabla_simulator(config_path,bin_path, bandwidth, precision, verbosity)
    cycles = t.simulate()
    print ("Compute cycles = {0}".format(cycles))
