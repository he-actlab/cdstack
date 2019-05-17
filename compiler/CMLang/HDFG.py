import networkx as nx
import os
import pprint
from CMLang.Component import Component, Node





class HDFG:

    def __init__(self,fname, compiler, tree,
            print_code=True,
            commented=True):

        self.fname = fname
        self.compiler = compiler
        self.instance_counts = {}
        self.instances = {}
        self.definitions = {}
        self.declarations = {}
        self.ir = []
        self.flows = {}
        self.flows['count'] = 0
        self.tree = tree
        self.commented = commented
        self.edges = {}
        self.nodes = {}
        self.scope = []

        self.generate_IR()

        if print_code:
            self.print_code()


    def create_graph(self):
        assert 'main' in self.compiler.component_def.keys()

        # Add main declaration flows to scope
        for f in self.definitions['main'].flows:
            self.flows[f['local_name']] = self.flows['count']
            self.flows['count'] += 1

            # instruction = '\tedge c{}, {}'.format(arg, declaration_args[arg][0])
            # # comment = ''.format(map_name, declaration_args[arg][0])
            # if self.commented:
            #     self.instances[dec]['body'].append('{:<40s} ; {:<45s}'.format(instruction, comment))
            # else:
            #     self.instances[dec]['body'].append('{:<40s}'.format(instruction))
            # continue
            # print(self.definitions['main']['body'])

        main_instances = self.compiler.component_def['main']['instances']
        for dec in main_instances:

            self.create_instance(dec, 'main')

            # Get the arguments given to the component instance
            declaration_args = self.compiler.component_inst[dec]['args']

            # Get the arguments given to the component definition for mapping
            declaration_definition = self.compiler.component_def[dec.split('$')[0]]['args']

            # Iterate over the arguments of the instance, mapping to the component declaration
            for arg in range(len(declaration_args)):
                # Positional argument in definition
                map_name, carg = next(
                    ((name, carg) for name, carg in declaration_definition.items() if carg['position'] == arg), None)
                # Positional argument in instance call
                instance_scope = dec + ':' + map_name
                if carg['edge_type'] == 'parameter' and declaration_args[arg][1] == 'number':
                    instruction = '\tconnect c{}, {}'.format(arg, declaration_args[arg][0])
                    comment = '{} -> {}'.format(map_name, declaration_args[arg][0])
                    if self.commented:
                        self.instances[dec]['body'].append('{:<40s} ; {:<45s}'.format(instruction, comment))
                    else:
                        self.instances[dec]['body'].append('{:<40s}'.format(instruction))
                    continue

                mapped_scope = declaration_args[arg][0]
                self.flows[instance_scope] = self.flows[mapped_scope]
                instruction = '\tconnect c{}, q{}'.format(arg, self.flows[instance_scope])
                comment = '{} -> {}'.format(declaration_args[arg][0], map_name)
                if self.commented:
                    self.instances[dec]['body'].append('{:<40s} ; {:<45s}'.format(instruction, comment))
                else:
                    self.instances[dec]['body'].append('{:<40s}'.format(instruction))

            self.create_node(dec)

    def create_node(self, component_instance):
        # Get the definition of the component instance
        component_name = component_instance.split('$')[0]
        component = self.compiler.component_def[component_name]

        # Create node for component instance in graph
        self.nodes[component_instance] = {}
        self.nodes[component_instance]['subcomponents'] = []

        # Add the current scope
        self.scope.append(component_instance)




        # We need to iterate over the declared flows in the scope and create queues associated with them
        for f in self.definitions[component_name].flows:
            self.flows[':'.join(map(str,self.scope)) + ':' + f['local_name']] = self.flows['count']
            self.flows['count'] += 1


        # Iterate over each declared component instance, performing DFS on each
        for dec in component['instances']:

            # Create an the instance for instruction writing
            self.create_instance(dec, self.compiler.component_inst[dec]['parent'])

            # Need to add the instance declaration to the instructions

            # Get the arguments given to the component instance
            declaration_args = self.compiler.component_inst[dec]['args']

            # Get the arguments given to the component definition for mapping
            declaration_definition =  self.compiler.component_def[dec.split('$')[0]]['args']

            # Iterate over the arguments of the instance, mapping to the component declaration

            #TODO: Check for unequal arg counts for parameter setting
            for arg in range(len(declaration_args)):

                # Positional argument in definition
                name, carg = next(
                    ((name,carg) for name, carg in declaration_definition.items() if carg['position'] == arg), None)

                if carg['edge_type'] == 'parameter' and declaration_args[arg][1] =='number':
                    instruction = '\tconnect c{}, {}'.format(arg,declaration_args[arg][0])
                    comment = '{} -> {}'.format(name, declaration_args[arg][0])
                    if self.commented:
                        self.instances[dec]['body'].append('{:<40s} ; {:<45s}'.format(instruction, comment))
                    else:
                        self.instances[dec]['body'].append('{:<40s}'.format(instruction))
                    continue

                # Positional argument in instance call
                instance_scope = ':'.join(map(str, self.scope)) + ':' + dec + ':' + name


                mapped_scope = ':'.join(map(str,self.scope)) + ':' + declaration_args[arg][0]
                self.flows[instance_scope] = self.flows[mapped_scope]

                instruction = '\tconnect c{}, q{}'.format(arg, self.flows[instance_scope])
                comment = '{} -> {}'.format(declaration_args[arg][0], name)
                if self.commented:
                    self.instances[dec]['body'].append('{:<40s} ; {:<45s}'.format(instruction, comment))
                else:
                    self.instances[dec]['body'].append('{:<40s}'.format(instruction))


            self.create_node(dec)


        del self.scope[-1]


    ## TODO: Write to file instead of print
    def generate_IR(self):
        file_path, extension = os.path.splitext(self.fname)
        self.program = file_path.split("/")[-1]
        ir_file = file_path + ".avm"

        self.generate_definitions()
        self.create_graph()


    def create_instance(self, component_instance, parent):

        self.instances[component_instance] = {}
        self.instances[component_instance]['body'] = []
        self.instances[component_instance]['end'] = ".cend"
        header = ".cbegin " + component_instance
        if len(self.scope) > 0:
            comment = "parent: {}".format(self.scope[-1])
        else:
            comment = "parent: {}".format(parent)

        if self.commented:
            self.instances[component_instance]['start'] = '{:<40s} \t; {:<45s}'.format(header, comment)
        else:
            self.instances[component_instance]['start'] = '{:<40s}'.format(header)

    def generate_definitions(self):

        for name in self.compiler.component_def.keys():
            new = Component(name,
                            self.compiler.component_def[name],
                            self.flows['count'], self.tree,
                            self.compiler.flows,
                            self.commented)
            self.definitions[name] = new


    def print_code(self):


        for inst in self.instances.keys():
            print(self.instances[inst]['start'])
            for body in self.instances[inst]['body']:
                print(body)
            print(self.instances[inst]['end'])
            print("\n")

        for name in self.definitions.keys():
            print(self.definitions[name].start)

            for head in self.definitions[name].header:
                print(head)

            for body in self.definitions[name].body:
                print(body)

            for foot in self.definitions[name].footer:
                print(foot)

            print(self.definitions[name].end)
            print("\n")




