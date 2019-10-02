import os

import onnx
from hdfg import hdfgutils, load_store
from hdfg.hdfg_pb2 import *
from hdfg.onnx_hdfg.tools import net_drawer


class ONNXCMStack():

    def __init__(self, onnx_proto):
        self.input_proto = onnx_proto
        self.output_dir, self.output_file = os.path.split(self.input_proto)
        self.proto_name = self.output_file.split('.')[0]
        self.components = {}
        self.edges = {}

    def add_component(self, name):
        if name not in self.components.keys():
            self.components[name] = len(self.components.keys())
    def add_edge(self, name):
        if name not in self.edges.keys():
            self.edges[name] = len(self.edges.keys())

    def run(self):
        self.model = onnx.load(self.input_proto)
        self.graph = self.model.graph
        # self.visualize_onnx_format()
        self.create_program()
        outfile = self.output_dir + '/' + self.proto_name + '.pb'
        load_store.save_program(self.cmstack_program,outfile)

    def create_program(self):

        self.cmstack_program = Program(name=self.proto_name)
        self.cmstack_program.producer_name = 'onnx'
        for des in self.model.DESCRIPTOR.fields:
            if des.name not in ['graph', 'metadata_props', 'opset_import']:
                value = getattr(self.model,des.name)
                attribute = hdfgutils.make_attribute(des.name, value)
                self.cmstack_program.attributes[des.name].CopyFrom(attribute)

        for mdata in self.model.metadata_props:
            attribute = hdfgutils.make_attribute(mdata.key, mdata.value)
            self.cmstack_program.attributes[mdata.key].CopyFrom(attribute)

        domain_ops = []
        for op in self.model.opset_import:
            domain = op.domain
            version = str(op.version)
            if len(domain) == 0 or len(version) == 0:
                continue
            domain_ops.append(domain)
            domain_ops.append(version)
        domain_attr = hdfgutils.make_attribute('opset_import', domain_ops)
        self.cmstack_program.attributes['opset_import'].CopyFrom(domain_attr)

        self.create_graph()

    def create_graph(self):
        cmstack_graph = self.cmstack_program.graph
        if 'name' in self.graph.DESCRIPTOR.fields_by_name.keys():
            cmstack_graph.name = self.graph.name
        else:
            cmstack_graph.name = self.proto_name
        inames = []
        for i in self.graph.input:
            new_edge = ValueInfo(name=i.name)
            inames.append(i.name)
            self.make_value_info_type(i, new_edge)
            self.add_edge(i.name)
            new_edge.gid = self.edges[i.name]

            cmstack_graph.edge_info[i.name].CopyFrom(new_edge)
        cmstack_graph.input.extend(inames)

        onames = []
        for o in self.graph.output:
            onames.append(o.name)
            new_edge = ValueInfo(name=o.name)

            self.make_value_info_type(o, new_edge)
            self.add_edge(o.name)
            new_edge.gid = self.edges[o.name]

            cmstack_graph.edge_info[o.name].CopyFrom(new_edge)
        cmstack_graph.output.extend(onames)

        for v in self.graph.value_info:
            if v.name in cmstack_graph.edge_info:
                continue

            new_edge = ValueInfo(name=v.name)

            self.make_value_info_type(v, new_edge)
            self.add_edge(v.name)
            new_edge.gid = self.edges[v.name]

            cmstack_graph.edge_info[v.name].CopyFrom(new_edge)

        for init in self.graph.initializer:
            cmstack_init = cmstack_graph.initializer.add()
            self.make_tensor(init, cmstack_init)

        for n in self.graph.node:
            component = cmstack_graph.sub_graph.add()
            self.make_node(n, component)
            self.add_component(component.name)
            component.gid = self.components[component.name]

    def make_node(self, node, component):
        component.input.extend(node.input)
        component.output.extend(node.output)
        component.name = node.name
        component.doc_string = node.doc_string
        component.op_type = node.op_type
        component.op_cat = 'leaf'
        if len(node.domain) > 0:
            domain_attr = hdfgutils.make_attribute('domain', node.domain)
            component.attributes['domain'].CopyFrom(domain_attr)

        self.make_attributes(node, component)

    def make_value_info_type(self, value_info, edge_info):

        tensor = value_info.type.tensor_type
        edge_info.type.tensor_type.elem_type = tensor.elem_type

        edge_shape = edge_info.type.tensor_type.shape

        for d in tensor.shape.dim:
            dim = edge_shape.dim.add()

            if d.dim_param:
                dim.dim_param = d.dim_param
            elif d.dim_value:
                dim.dim_value = d.dim_value

            if d.denotation:
                dim.denotation = d.denotation

    def make_attributes(self, node, component):

        for att in node.attribute:
            val = onnx.helper.get_attribute_value(att)
            key = att.name
            if len(att.ref_attr_name) > 0:
                ref_attr = hdfgutils.make_attribute('ref_attr_name', att.ref_attr_name)
                component.attributes['ref_attr_name'].CopyFrom(ref_attr)
            val_attr = hdfgutils.make_attribute(key, val)
            component.attributes[key].CopyFrom(val_attr)

    def make_tensor(self, input_tensor, cmstack_tensor):

        cmstack_tensor.dims.extend(input_tensor.dims)
        cmstack_tensor.data_type = input_tensor.data_type

        cmstack_tensor.segment.begin = input_tensor.segment.begin
        cmstack_tensor.segment.end = input_tensor.segment.end
        cmstack_tensor.doc_string = input_tensor.doc_string
        cmstack_tensor.name = input_tensor.name
        for ex in input_tensor.external_data:
            cmstack_tensor.external_data[ex.key] = ex.value

        cmstack_tensor.data_location = input_tensor.data_location

        if input_tensor.raw_data:
            cmstack_tensor.raw_data.extend(input_tensor.raw_data)
        elif input_tensor.float_data:
            cmstack_tensor.float_data.extend(input_tensor.float_data)
        elif input_tensor.int32_data:
            cmstack_tensor.int32_data.extend(input_tensor.int32_data)
        elif input_tensor.string_data:
            cmstack_tensor.string_data.extend(input_tensor.string_data)
        elif input_tensor.int64_data:
            cmstack_tensor.int64_data.extend(input_tensor.int64_data)
        elif input_tensor.uint64_data:
            cmstack_tensor.uint64_data.extend(input_tensor.uint64_data)
        elif input_tensor.double_data:
            cmstack_tensor.double_data.extend(input_tensor.double_data)


    def visualize_onnx_format(self):
        graph = net_drawer.GetPydotGraph(
            self.graph,
            name=self.graph.name,
            rankdir="TB",
            node_producer=net_drawer.GetOpNodeProducer(
                embed_docstring=True,
                **net_drawer.OP_STYLE
            ),
        )
        filename =self.output_dir + '/' + self.proto_name + '.dot'
        graph.write(filename, format='raw')
        png_filename = filename[:-3] + 'png'
        try:
            graph.write_png(png_filename)
        except Exception:
            print(
                'Error when writing out the pdf file. Pydot requires graphviz '
                'to convert dot files to pdf, and you may not have installed '
                'graphviz. On ubuntu this can usually be installed with "sudo '
                'apt-get install graphviz". We have generated the .dot file '
                'but will not be able to generate pdf file for now.'
            )





