import os
import onnx
from shutil import copyfile
from hdfg import hdfgutils
from hdfg import load_store
from hdfg.passes.flatten import flatten_graph, is_literal
import codegen as c
from hdfg.hdfg_pb2 import Component, Program
from hdfg.visualize import *
from .serial.DataFlowGraph import *
from codegen.tabla import tabla_utils

def read_config(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return json.loads(contents)

class TablaTranslation(object):
    func_table = {
        'pi' : 2,
        'sum' : 2,
        'norm' : 2,
        'gaussian' : 1,
        'sigmoid' : 1,
        'sig_sym' : 1,
        'log' : 1
    }
    op_map = {
        "sub" : "-",
        "add" : "+",
        "div" : "/",
        "mul" : "*",
        "sigmoid" : "sigmoid",
        "sum" : "sum",
        "tlt" : "<",
        "tgt" : ">",
    }


    def __init__(self, onnx_proto, run_async=False):
        self.input_proto = onnx_proto
        self.output_dir, self.output_file = os.path.split(self.input_proto)
        self.proto_name = self.output_file.split('.')[0]
        self.program = load_store.load_program(self.input_proto)
        self.graph = self.program.graph
        self.templates = self.program.templates
        self.components = {}
        self.includes = []
        self.functions = []
        self.structs = []
        self.signature_map = {}
        self.initializer = None
        self.header = []
        self.exec = []
        self.run_async = run_async
        self.add_flattened_graph()
        # self.visualize()
        self.create_node_map()

        self.dfg = DataFlowGraph()

        # Create source and sink nodes first.
        source = DFGNode()
        source.operation = 'source'
        self.dfg.add(source)

        sink = DFGNode()
        sink.operation = 'sink'
        sink.dist2sink = 0
        self.dfg.add(sink)

        self.translate_graph()
        self.set_d2sink(sink)
        removedNodes = []
        for node in self.dfg.nodes:
            if node.dist2sink is None:
                for child in node.children:
                    child.parents.remove(node)
                for parent in node.parents:
                    parent.children.remove(node)
                removedNodes.append(node)
        for node in removedNodes:
            self.dfg.remove(node)
        self.dfg.updateId()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(dir_path + '/artifacts/'):
            os.makedirs(dir_path + '/artifacts/')
        macro_dfg_file = dir_path + '/artifacts/macro_dfg.json'
        self.write_dfg(macro_dfg_file)
        tabla_utils.compile(self.dfg)

    def write_dfg(self, path):
        self.dfg.save(path)



    def create_dfg(self):
        for sg in self.flattened_graph.statement_graphs:
            nodes = sg.statement_node
            node_cats = [self.node_map[n].op_cat for n in nodes]
            if 'assign' in node_cats:
                self.idx_map = {}
                if node_cats[-1] == 'read_write':
                    assign_node = self.node_map[nodes[-2]]
                    assignee_edge = self.flattened_graph.edge_info[self.node_map[nodes[-2]].output[0]]
                    context, var = self.get_var_context(assignee_edge.name)
                    assignee_key = nodes[-1]
                else:
                    assign_node = self.node_map[nodes[-1]]
                    assignee_edge = self.flattened_graph.edge_info[self.node_map[nodes[-1]].output[0]]
                    context, var = self.get_var_context(assignee_edge.name)
                    assignee_key = context + '/' + str(assignee_edge.vid)


                if assignee_edge.iid:
                    iid = assignee_edge.iid
                    if iid in list(self.flattened_graph.edge_info):
                        iid_info = self.flattened_graph.edge_info[iid]
                    elif (context + "/" + iid) in list(self.flattened_graph.edge_info):
                        iid_info = self.flattened_graph.edge_info[context + "/" + iid]
                    else:
                        logging.error("Index id not in edge map: context {}, id: {}".format(context, iid))
                    dimensions = hdfgutils.get_attribute_value(iid_info.attributes['dimensions'])

                    if len(dimensions) == 0:
                        dimensions.append(iid)
                    node_strings = self.generate_index_nodes([assignee_key], dimensions, context, '')
                else:
                    node_strings = [assignee_key]
                result = self.create_statement_nodes(nodes)

                if len(result) != len(node_strings):
                    print("Assignee key for unequal nodes: {}".format(assignee_key))
                else:
                    var_id = var[:var.find('[')]
                    if var_id in self.gradient_table.keys():
                        dtype = 'gradient'
                    else:
                        dtype = result[0].dataType
                    if assignee_key not in self.symbol_table.keys():
                        self.symbol_table[assignee_key] = []
                    for n in range(len(node_strings)):
                        result[n].dataType = dtype
                        self.symbol_table[assignee_key].append(result[n])
        for key in self.symbol_table.keys():       # Connect outputs
            if key in list(self.flattened_graph.state):
                for node in self.symbol_table[key]:
                    if len(node.children) is 0 and len(node.parents) is not 1:
                        node.dataType = 'model'
                        self.connect_node(node, self.dfg.get(1))

    def create_statement_nodes(self, nodes):
        result = []
        for n in nodes:
            node_info = self.node_map[n]

            if node_info.op_type in self.op_map.keys():
                if len(node_info.input) > 2:
                    logging.error("Too many inputs for TABLA op - Node: {}, op: {}".format(n, node_info.op_type))
                elif node_info.op_type in self.func_table.keys():
                    self.create_func_node(node_info)
                else:
                    self.create_bin_node(node_info)
                if node_info.output[0] not in self.symbol_table.keys():
                    logging.error("Output {} not in symbol table".format(node_info.output[0]))
                    exit(0)
                else:
                    result = self.symbol_table[node_info.output[0]]

        return result

    def create_func_node(self,node):

        if node.op_type == 'sum':
            expr = self.get_node(node.input[0])
            acc_range = node.input[1]
            result = self.accum_nodes('+', expr, node.output[0])
            self.symbol_table[node.output[0]] = [result]
        elif node.op_type == 'sigmoid':

            parent = self.get_node(node.input[0])
            dfg_node = DFGNode()
            dfg_node.operation = node.op_type
            dfg_node.name = node.output[0]
            self.dfg.add(dfg_node)
            self.connect_node(parent[0], dfg_node)
            self.symbol_table[node.output[0]] = [dfg_node]

    def accum_nodes(self,op, nodes, name):
        if len(nodes) == 1:
            return nodes[0]
        elif len(nodes) == 2:
            node = DFGNode()
            node.operation = op
            node.name =name
            self.dfg.add(node)
            self.connect_node(nodes[0], node)
            self.connect_node(nodes[1], node)
            return node
        else:
            middle = len(nodes)//2
            left = nodes[middle:]
            right = nodes[:middle]
            node = DFGNode()
            node.operation = op
            node.name= name
            self.dfg.add(node)
            self.connect_node(self.accum_nodes(op, left, name), node)
            self.connect_node(self.accum_nodes(op, right, name), node)
            return node

    def create_bin_node(self,node):
        left = self.get_node(node.input[0])
        right = self.get_node(node.input[1])
        op = self.op_map[node.op_type]
        dst = node.output[0]
        contextleft, varleft = self.get_var_context(node.input[0])
        contextright, varright = self.get_var_context(node.input[1])
        varleft = varleft[:varleft.find('[')]
        varright = varright[:varright.find('[')]

        if varleft in self.gradient_table.keys():
            dtype = 'gradient'
        elif varright in self.gradient_table.keys():
            dtype = 'gradient'
        else:
            dtype = None
        indices_left =node.input[0].count('[')
        indices_right =node.input[1].count('[')
        if dst in self.symbol_table.keys():
            logging.error("Dst already in symbol table: {}".format(dst))
        else:
            self.symbol_table[dst] = []
        if indices_left > 0:
            lindex = []
            ltext = node.input[0]
            while ltext.find('[') != -1:
                lindex.append(ltext[ltext.find('[')+1:ltext.find(']')])
                ltext = ltext[ltext.find(']')+1:]

        if indices_right > 0:
            rindex = []
            rtext = node.input[1]
            while rtext.find('[') != -1:
                rindex.append(rtext[rtext.find('[')+1:rtext.find(']')])
                rtext = rtext[rtext.find(']')+1:]

        if len(left) == 1 and len(right) > 1:

            for n in range(len(right)):
                dfg_node = DFGNode()
                dfg_node.operation = op
                dfg_node.name = node.output[0]
                dfg_node.dataType = dtype
                self.dfg.add(dfg_node)
                self.connect_node(left[0], dfg_node)
                self.connect_node(right[n], dfg_node)
                self.symbol_table[dst].append(dfg_node)
        elif len(right) == 1 and len(left) > 1:
            for n in range(len(left)):
                dfg_node = DFGNode()
                dfg_node.operation = op
                dfg_node.name = node.output[0]
                dfg_node.dataType = dtype

                self.dfg.add(dfg_node)
                self.connect_node(left[n], dfg_node)
                self.connect_node(right[0], dfg_node)
                self.symbol_table[dst].append(dfg_node)
        elif len(left) != len(right):
            if indices_left == indices_right:
                for l in left:
                    for r in right:
                        dfg_node = DFGNode()
                        dfg_node.operation = op
                        dfg_node.name = node.output[0]

                        dfg_node.dataType = dtype

                        self.dfg.add(dfg_node)
                        self.connect_node(l, dfg_node)
                        self.connect_node(r, dfg_node)
                        self.symbol_table[dst].append(dfg_node)
            elif indices_right > indices_left:
                lval = 0
                for r in (right):
                    if lval == len(left):
                        lval = 0
                    dfg_node = DFGNode()
                    dfg_node.operation = op
                    dfg_node.name = node.output[0]

                    dfg_node.dataType = dtype

                    self.dfg.add(dfg_node)
                    self.connect_node(left[lval], dfg_node)
                    self.connect_node(r, dfg_node)
                    self.symbol_table[dst].append(dfg_node)
                    lval +=1
            else:
                rval = 0
                for l in (left):
                    if rval == len(right):
                        rval = 0
                    dfg_node = DFGNode()
                    dfg_node.operation = op
                    dfg_node.name = node.output[0]

                    dfg_node.dataType = dtype

                    self.dfg.add(dfg_node)
                    self.connect_node(right[rval], dfg_node)
                    self.connect_node(l, dfg_node)
                    self.symbol_table[dst].append(dfg_node)
                    rval +=1
        else:
            for n in range(len(left)):
                dfg_node = DFGNode()
                dfg_node.operation = op
                dfg_node.name = node.output[0]

                dfg_node.dataType = dtype

                self.dfg.add(dfg_node)
                self.connect_node(left[n], dfg_node)
                self.connect_node(right[n], dfg_node)
                self.symbol_table[dst].append(dfg_node)

    def get_node(self, edge):

        if is_literal(edge):
            if edge not in self.symbol_table.keys():
                node = DFGNode()
                node.operation = edge
                node.name = edge
                node.dataType = 'constant'
                self.dfg.add(node)
                self.connect_node(self.dfg.get(0), node)
                self.symbol_table[edge] = [node]
                return self.symbol_table[edge]
            else:
                return self.symbol_table[edge]
        elif edge in self.symbol_table.keys():
            return self.symbol_table[edge]
        else:
            edge_info =self.flattened_graph.edge_info[edge]
            if 'alias' in list(edge_info.attributes):
                alias = hdfgutils.get_attribute_value(edge_info.attributes['alias'])
                print("Alias is: {}".format(alias))
            vid = edge_info.vid
            context, var = self.get_var_context(edge)
            if edge_info.iid:
                iid = edge_info.iid
                if iid in list(self.flattened_graph.edge_info):
                    iid_info = self.flattened_graph.edge_info[iid]
                elif (context + "/" + iid) in list(self.flattened_graph.edge_info):
                    iid_info = self.flattened_graph.edge_info[context + "/" + iid]
                else:
                    logging.error("Index id not in edge map: context {}, id: {}".format(context, iid))
                dimensions = hdfgutils.get_attribute_value(iid_info.attributes['dimensions'])
                if len(dimensions) == 0:
                    dimensions.append(iid)
                _ = self.generate_index_nodes([''], dimensions, context, '')
                vid_hash = context + '/' + vid
                if len(self.symbol_table[vid_hash]) != len(self.idx_map[iid]):
                    logging.error("Trying to use wrong dimensional input for: {} with index {}, {} and {} ".format(vid, iid,  len(self.symbol_table[vid_hash]),len(self.idx_map[iid]) ))
                    exit(1)
                else:
                    self.symbol_table[edge] = self.symbol_table[vid_hash].copy()
                    return self.symbol_table[edge]
            else:
                print(self.symbol_table.keys())
                logging.error("Error, edge not found in symbol table and doesnt have index: {}, vid: {} edge name: {}".format(edge, vid, edge_info.name))




    def create_node_map(self):
        self.node_map = {}
        for n in self.flattened_graph.sub_graph:
            self.node_map[n.name] = n

    def translate_graph(self):
        self.link_table = {}
        self.const_table = {}
        self.iter_table = {}
        self.symbol_table = {}
        self.gradient_table = {}
        self.create_constant_table()
        self.create_iter_table()
        self.create_symbol_table()
        self.create_gradient_table()
        self.create_dfg()

    def add_flattened_graph(self):
        self.flattened_graph = Component(name="flattened_" + str(self.proto_name))
        edge_node_ids = {'edges': {},
                         'nodes': {}}
        self.flattened_graph.statement_graphs.extend([])
        flatten_graph(self.flattened_graph, self.graph, self.templates, '', edge_node_ids, {})
        flattened_graph_attr = hdfgutils.make_attribute('flattened', self.flattened_graph)
        self.program.attributes['flattened_graph'].CopyFrom(flattened_graph_attr)

    def visualize(self):
        rankdir = "TB"
        pydot_graph = pydot.Dot(name=self.input_proto, rankdir=rankdir)

        out_graph = GetPydotGraph(self.flattened_graph, name=self.graph.name, rankdir=rankdir)
        filename = self.output_dir + '/' + self.output_file[:-3] + '.dot'
        pydot_graph.add_subgraph(out_graph)

        pydot_graph.write(filename, format='raw')
        pdf_filename = filename[:-3] + 'png'
        try:
            pydot_graph.write_png(pdf_filename)

        except Exception:
            print(
                'Error when writing out the png file. Pydot requires graphviz '
                'to convert dot files to pdf, and you may not have installed '
                'graphviz. On ubuntu this can usually be installed with "sudo '
                'apt-get install graphviz". We have generated the .dot file '
                'but will not be able to generate png file for now.'
            )

    def create_constant_table(self):
        for e in list(self.flattened_graph.edge_info):
            edge = self.flattened_graph.edge_info[e]
            vtype = hdfgutils.get_attribute_value(edge.attributes['vtype'])
            dtype = hdfgutils.get_attribute_value(edge.attributes['type'])
            if 'alias' in list(edge.attributes) and vtype == 'scalar':

                context, var = self.get_var_context(e)

                if context not in self.const_table.keys():
                    self.const_table[context] = {}

                alias = hdfgutils.get_attribute_value(edge.attributes['alias'])
                if var not in self.const_table[context].keys():
                    if dtype  == 'int':
                        self.const_table[context][var] = int(alias)
                    elif dtype == 'float':
                        self.const_table[context][var] = float(alias)
                    else:
                        self.const_table[context][var] = alias

    def create_gradient_table(self):
        for sg in self.flattened_graph.statement_graphs:
            nodes = sg.statement_node
            node_cats = [self.node_map[n].op_cat for n in nodes]

            if node_cats[-1] == 'read_write':
                assignee_edge = self.flattened_graph.edge_info[self.node_map[nodes[-1]].output[0]]
                assignee_key = nodes[-1]
            else:
                continue
            assignee_update = False
            gradient = None
            gradient_key = None
            for n in nodes:
                node_info = self.node_map[n]
                if n == assignee_key:
                    assignee_update = True
                else:
                    cat = node_info.op_cat

                for i in node_info.input:
                    if i in list(self.flattened_graph.edge_info):
                        in_edge = self.flattened_graph.edge_info[i]
                        vcat = hdfgutils.get_attribute_value(in_edge.attributes['vcat'])
                        if vcat == 'assign':
                            gradient = in_edge.name
                            gradient_key = in_edge.vid

            if assignee_update and gradient:
                self.gradient_table[gradient_key] = True
                self.link_table[gradient] = assignee_key

    def create_iter_table(self):
        for e in list(self.flattened_graph.edge_info):
            edge = self.flattened_graph.edge_info[e]
            vtype = hdfgutils.get_attribute_value(edge.attributes['vtype'])
            vcat = hdfgutils.get_attribute_value(edge.attributes['vcat'])

            if vcat == 'declaration' and vtype == 'index':
                context = "/".join(e.split('/')[:-1])

                lower = hdfgutils.get_attribute_value(edge.attributes['lower'])
                upper = hdfgutils.get_attribute_value(edge.attributes['upper'])
                lower_val = self.try_eval(lower, context)
                upper_val = self.try_eval(upper, context)
                if not is_literal(str(lower_val)):
                    logging.error("Error, indices not evaluated for {}, lower val {}".format(e, lower))

                if not is_literal(str(upper_val)):
                    logging.error("Error, indices not evaluated for {}, upper val {}".format(e, upper))

                self.iter_table[e] = (lower_val, upper_val)

    def create_symbol_table(self):
        for c in self.const_table.keys():
            for k in self.const_table[c].keys():
                const = c + '/' + k
                node = DFGNode()
                node.operation = const
                node.name = const
                node.dataType = 'constant'
                self.dfg.add(node)
                self.connect_node(self.dfg.get(0), node)
                self.symbol_table[const] = [node]

        for ename in list(self.flattened_graph.edge_info):
            context, var = self.get_var_context(ename)
            context_expr = context + "/" + var
            if var in list(self.flattened_graph.edge_info):
                e = var
                edge = self.flattened_graph.edge_info[var]
            elif context_expr in list(self.flattened_graph.edge_info):
                e = context_expr
                edge = self.flattened_graph.edge_info[context_expr]

            else:
                logging.error("Error! Edge name not in edge map: {}, context: {}".format(var, context))

            vtype = hdfgutils.get_attribute_value(edge.attributes['vtype'])
            vcat = hdfgutils.get_attribute_value(edge.attributes['vcat'])

            if e in self.flattened_graph.input or e in self.flattened_graph.state:
                if e in self.flattened_graph.input:
                    dtype = 'model_input'
                elif e in self.flattened_graph.state:
                    dtype = 'model'

                dims = hdfgutils.get_attribute_value(edge.attributes['dimensions'])
                if len(dims) == 0:
                    if 'alias' in list(edge.attributes):
                        name = hdfgutils.get_attribute_value(edge.attributes['alias'])
                    else:
                        name = e
                    node = DFGNode()
                    node.operation = name
                    node.dataType = dtype
                    self.dfg.add(node)
                    self.connect_node(self.dfg.get(0), node)
                    self.symbol_table[name] = [node]
                else:
                    iters = []
                    for d in dims:
                        if d.isdigit():
                            iter = int(d)
                            iters.append(iter)
                        elif d in self.const_table[context].keys():
                            iter = self.const_table[context][d]
                            iters.append(iter)
                        else:
                            logging.error("Dimension not in constants: {}".format(d))
                    node_strings = self.generate_array_nodes([e], iters)
                    self.symbol_table[e] = []
                    for n in node_strings:
                        node = DFGNode()
                        node.operation = n
                        node.name = n
                        node.dataType = dtype
                        self.dfg.add(node)
                        self.connect_node(self.dfg.get(0), node)
                        self.symbol_table[e].append(node)


    def generate_array_nodes(self,nodes, iters):
        if len(iters) == 0:
            return nodes
        else:
            current_iter = iters[0]
            new_nodes = []
            for n in nodes:
                for i in range(current_iter):
                    key = n + '[' + str(i) + ']'
                    new_nodes.append(key)
            return self.generate_array_nodes(new_nodes, iters[1:])


    def generate_index_nodes(self,nodes, iters, context, multi_index):
        if len(iters) == 0:
            return nodes
        else:
            curr = iters[0]
            update_index = True
            if curr not in self.idx_map.keys():
                self.idx_map[curr] = []
            else:
                update_index = False
            multi_index += '[' + curr + ']'

            if multi_index not in self.idx_map.keys():
                self.idx_map[multi_index] = []
            else:
                return self.generate_index_nodes(self.idx_map[multi_index], iters[1:], context, multi_index)

            if curr in self.const_table[context].keys():
                low = self.const_table[context][curr]
                high = self.const_table[context][curr] + 1
            elif curr.isdigit():
                low = int(curr)
                high = low + 1
            elif curr in self.iter_table.keys():
                low, high = self.iter_table[curr]
            elif context + "/" + curr in self.iter_table.keys():
                low, high = self.iter_table[context + "/" + curr]
            else:
                logging.error("Could not find index for {}".format(curr))
            new_nodes = []
            for n in nodes:

                for i in range(low, high+1):
                    key = n + '[' + str(i) + ']'
                    indices = key[key.find('['):]
                    self.idx_map[multi_index].append(indices)
                    new_nodes.append(key)
                    if update_index:
                        self.idx_map[curr].append('[' + str(i) + ']')
                update_index = False
            return self.generate_index_nodes(new_nodes, iters[1:], context, multi_index)

    def connect_node(self, parent, child):

        child.parents.insert(0, parent)
        parent.children.append(child)


    def get_var_context(self, expr):
        context = expr.split("/")
        if len(context) > 1:
            var = context[-1]
            context = "/".join(context[:-1])
        else:
            var = context[0]
            context = "main"
        return context, var

    def try_eval(self, expr, context):
        context_expr = context + "/" + expr
        if expr in list(self.flattened_graph.edge_info):
            edge_expr = self.flattened_graph.edge_info[expr]
        elif context_expr in list(self.flattened_graph.edge_info):
            edge_expr = self.flattened_graph.edge_info[(context_expr)]
        else:
            print("Error! No expression in edges: {}".format(expr))

        vtype = hdfgutils.get_attribute_value(edge_expr.attributes['vtype'])
        if vtype == 'scalar':
            return int(expr)
        else:
            result = eval(expr, self.const_table[context].copy())

            return result

    def set_d2sink(self, curr_node):
        for parent in curr_node.parents:
            if parent.dist2sink is None or parent.dist2sink < curr_node.dist2sink + 1:
                parent.dist2sink = curr_node.dist2sink + 1
            self.set_d2sink(parent)

