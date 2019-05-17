import json
from abc import abstractmethod
import graphviz
from Queue import Queue




class Component:
    id = 0
    def __init__(self, name,cmp_type, primitive):
        self.id  = Component.id
        Component.id += 1

        self.name = name
        self.cmp_type = cmp_type
        self.primitive = primitive
        self.sub_components = []
        self.init_flows = {}
        self.input_flows = {}
        self.output_flows = {}
        self.state_flows = {}
        self.parameter_flows = {}

        self.parent_component = None  # id of Component where this component belongs

    @abstractmethod
    def run(self,*args):
        pass

    def to_dict(self):
        return {'id' : self.id,
                'name' : self.name,
                'primitive' : self.primitive,
                'parameter_flows' : [f.id for f in self.parameter_flows],
                'output_flows' : [f.id for f in self.output_flows],
                'input_flows' : [f.id for f in self.input_flows],
                'state_flows' : [f.id for f in self.state_flows],
                'initialized_flows' : [f.id for f in self.init_flows],
                'sub_components' : [c.id for c in self.sub_components],
                'parent_component': self.parent_component}


    def insert_sub(self, component):
        component.parent_component = self.id
        self.sub_components.append(component)

    def create_flow(self, name, flow_type, size=None, dtype=None):

        self.init_flows[name] = Flow(name, self, flow_type, size, dtype)
        return self.init_flows[name]

    def add_output(self, flow):

        self.output_flows[flow.name] = flow
        self.output_flows[flow.name].set_output(self)

    def add_input(self, flow):

        self.input_flows[flow.name] = flow
        self.input_flows[flow.name].set_input(self)

    def add_state(self, flow):
        self.state_flows[flow.name] = flow

    def add_parameter(self, flow):
        self.parameter_flows[flow.name] = flow

    def get_output(self, name):
        return self.output_flows[name]

    def get_input(self, name):
        return self.input_flows[name]

    def get_parameter(self, name):
        return self.parameter_flows[name]

    def get_state(self, name):
        return self.state_flows[name]

    def enqueue_output(self, name, data):
        self.output_flows[name].enqueue(data)

    def enqueue_state(self, name, data):
        self.state_flows[name].enqueue(data)

    def dequeue_state(self, name):
        return self.state_flows[name].dequeue()

    def dequeue_input(self, name):
        return self.input_flows[name].dequeue()

    def dequeue_parameter(self, name):

        ## Need the parameter to remain in the queue:

        temp = self.parameter_flows[name].dequeue()
        self.parameter_flows[name].enqueue(temp)

        return temp

class Flow:
    id = 0
    def __init__(self, name, parent, flow_type, size=None, dtype=None):
        self.id = Flow.id
        Flow.id += 1
        self.name = name
        self.ftype = flow_type
        self.dtype = dtype
        self.size = size
        self.output_component = None
        self.input_component = None

        if self.ftype == 'parameter':
            self.size = 1

        self.queue = Queue()  # unbounded queue if size None
        self.parent_component = parent.id

    def set_dtype(self, dtype):
        self.dtype = dtype

    def set_size(self, size_list):
        self.size = size_list

    def enqueue(self, data):
        self.queue.put(data)

    def dequeue(self):
        return self.queue.get()

    # Add case for more than one input/output component
    def set_input(self, component):
        self.input_component = component

    def set_output(self, component):
        self.output_component = component

    def is_empty(self):
        return self.queue.empty()

    def to_dict(self):
        return {'id': self.id,
                'flow_type' : self.ftype,
                'dtype' : self.dtype,
                'size' : self.size,
                'queue': list(self.queue),
                'input_component' : self.input_component.id,
                'output_component' : self.output_component.id}



