class Node:
    type_map = {"int" : "i32",
                "float" : "float",
                "complex" : "cmp",
                "string": "string"}

    def __init__(self, id, operation, instance_name=None, predicate_register=None, predicate=None, op1=None,
                 op2=None, dest=None, op1_iter=None, op2_iter=None, dest_iter=None, valtype=None, optype=None,
                 dims=[], type=None, component_type=None, low=None, high=None, predicate_iterator=None):
        self.operation = operation
        self.instance_name = instance_name
        self.predicate_register = predicate_register
        self.predicate_iterator = predicate_iterator
        self.predicate = predicate
        self.op1 = op1
        self.op2 = op2
        self.dest = dest
        self.op1_iter = op1_iter
        self.op2_iter = op2_iter
        self.dest_iter = dest_iter
        self.valtype = valtype
        self.optype = optype
        self.dims = dims
        self.type = type
        self.component_type = component_type
        self.low = low
        self.high = high

    def create_instruction(self):

        assert self.operation, "No operation found"
        # assert self.component_type, "No component type found"

        self.instr = "\t" + self.operation


        #TODO: Construct types
        if self.predicate_register:
            self.add_predicate()

        if self.operation == 'wait':
            self.instr += ' ' + self.instance_name
        else:
            if self.dest:
                self.instr += " "
                self.add_target()
            if self.op1:
                self.instr += ", "
                self.add_op1()

        if self.op2:
            self.instr += ", "
            self.add_op2()

        return self.instr

    def construct_type(self):

        if len(self.dims) > 0:
            self.instr += " [" + self.dims[0] + " x " + self.type_map[self.type] + "]"

            for i in range(1,len(self.dims)):
                self.instr = "[" + self.dims[i] + " x " + self.instr + "]"
        else:
            self.instr += " " + self.type_map[self.type]


    def add_op1(self):

        if self.op1_iter:
            self.instr += self.op1_iter + "(" + self.op1 + ")"
        else:
            self.instr += self.op1

    def add_op2(self):

        if self.op2_iter:
            self.instr += self.op2_iter + "(" + self.op2 + ")"
        else:
            self.instr += self.op2

    def add_target(self):

        if self.dest_iter:
            self.instr += self.dest_iter + "(" + self.dest + ")"
        else:
            self.instr += self.dest

    def add_predicate(self):

        self.instr += "_" + self.predicate + "<"
        if self.predicate_iterator:
            self.instr += self.predicate_iterator + "(" + self.predicate_register + ")>"
        else:
            self.instr += self.predicate_register + ">"