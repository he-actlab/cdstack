import json
import logging
import os
from collections import defaultdict

from cmstack.hdfg import hdfgutils
from cmstack.hdfg import load_store

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


try:
    import pydot
except ImportError:
    logger.info(
        'Cannot import pydot, which is required for drawing a network. This '
        'can usually be installed in python with "pip install pydot". Also, '
        'pydot requires graphviz to convert dot files to pdf: in ubuntu, this '
        'can usually be installed with "sudo apt-get install graphviz".'
    )
    print(
        'net_drawer will not run correctly. Please install the correct '
        'dependencies.'
    )
    pydot = None

OP_STYLE = {
    'shape': 'box',
    'color': '#0F9D58',
    'style': 'filled',
    'fontcolor': '#FFFFFF'
}
QUEUE_STYLE = {'shape': 'octagon'}

CLUSTER_STYLE = {'bgcolor': '#DCDCDC',
                 'style': 'rounded',
                 'fontsize': '20.0',
                 'fontname': 'times bold'}

edge_ids = {}
node_ids = {}

def _escape_label(name):

    # json.dumps is poor man's escaping
    return json.dumps(name)


def GetOpNodeProducer(append_output, **kwargs):
    def ReallyGetOpNode(op, op_id):
        # if op.name:
        #     node_name = '%s/%s (op#%s)' % (op.name, op.op_type, op_id)
        # else:
        node_name = '%s (op#%s)' % (op.op_type, op_id)
        for id, input_name in enumerate(op.input):
            node_name += '\ninput' + str(id) + ' : ' + input_name

        for id, output_name in enumerate(op.output):
            node_name += '\noutput' + str(id) + ' : ' + output_name

        return pydot.Node(_escape_label('node' + str(op.gid)),label=_escape_label(node_name),
                          **kwargs)
    return ReallyGetOpNode


def GetBlobNodeProducer(**kwargs):
    def ReallyGetBlobNode(node_name, label):
        return pydot.Node(_escape_label(node_name),
                          label=_escape_label(label),
                          **kwargs)
    return ReallyGetBlobNode

def get_node_id(name):
    if name not in node_ids.keys():
        node_ids[name] = len(node_ids.keys())

    return str(node_ids[name])

def get_edge_id(name):
    if name not in edge_ids.keys():
        edge_ids[name] = len(edge_ids.keys())

    return str(edge_ids[name])

def GetPydotGraph(
    graph,
    name=None,
    inputs=None,
    include_state=False,
    rankdir='LR',
    op_node_producer=None,
    blob_node_producer=None,
    pairs=[]
):
    if op_node_producer is None:
        op_node_producer = GetOpNodeProducer(True, **OP_STYLE)
    if blob_node_producer is None:
        blob_node_producer = GetBlobNodeProducer(**QUEUE_STYLE)
    nodes = graph.sub_graph
    pydot_graph = pydot.Cluster(name, label=graph.op_type, **CLUSTER_STYLE)
    pydot_node_counts = defaultdict(int)
    for n in nodes:

        op_cat = n.op_cat
        if op_cat == 'argument':
            continue
        elif op_cat == 'component':
            node_args = hdfgutils.get_attribute_value(n.attributes['ordered_args'])

            pysubgraph = GetPydotGraph(n, n.name,inputs=node_args,rankdir=rankdir)
            pydot_graph.add_subgraph(pysubgraph)

        else:
            op_node = op_node_producer(n, n.gid)
            pydot_graph.add_node(op_node)
            for i in n.input:
                input_name = graph.edge_info[i].name
                if input_name not in edge_ids.keys():
                    input_node = blob_node_producer(
                        _escape_label(
                        'edge' + str(graph.edge_info[i].gid)),
                        label=_escape_label(input_name),
                    )
                    edge_ids[input_name] = input_node
                else:
                    input_node = edge_ids[input_name]
                pydot_graph.add_node(input_node)
                eid_hash = '(' + input_node.get_name() + "," + op_node.get_name()  + ')'
                backward_hash = '(' + op_node.get_name() + "," + input_node.get_name()  + ')'
                if eid_hash not in pairs:
                    pydot_graph.add_edge(pydot.Edge(input_node, op_node))
                    pairs.append(eid_hash)
                    pairs.append(backward_hash)
            for o in n.output:
                output_name = graph.edge_info[o].name
                if output_name in edge_ids:
                    # we are overwriting an existing blob. need to updat the count.
                    pydot_node_counts[output_name] += 1
                output_node = blob_node_producer(
                    _escape_label(
                        'edge' + str(graph.edge_info[o].gid)),
                    label=_escape_label(output_name),
                )
                edge_ids[output_name] = output_node
                pydot_graph.add_node(output_node)
                eid_hash = '(' + op_node.get_name()  + "," + output_node.get_name()  + ')'
                backward_hash = '(' + output_node.get_name() + "," + op_node.get_name()   + ')'
                if eid_hash not in pairs:
                    pydot_graph.add_edge(pydot.Edge(op_node, output_node))
                    pairs.append(eid_hash)
                    pairs.append(backward_hash)
                if graph.edge_info[o].iid and graph.edge_info[o].vid:
                    vid = graph.edge_info[o].vid
                    if vid in graph.output:
                        name = graph.edge_info[vid].name
                        vid_node = edge_ids[name]

                        eid_hash = '(' + output_node.get_name() + "," + vid_node.get_name() + ')'
                        backward_hash = '(' + vid_node.get_name() + "," + output_node.get_name() + ')'
                        if eid_hash not in pairs:
                            pydot_graph.add_edge(pydot.Edge(output_node, vid_node))
                            pairs.append(eid_hash)
                            pairs.append(backward_hash)
            if include_state:
                for s in n.state:
                    state_name = graph.edge_info[s].name
                    if state_name in edge_ids:
                        # we are overwriting an existing blob. need to updat the count.
                        pydot_node_counts[state_name] += 1
                    state_node = blob_node_producer(
                        _escape_label(
                            'edge' + str(graph.edge_info[s].gid)),
                        label=_escape_label(state_name),
                    )
                    edge_ids[state_name] = state_node
                    pydot_graph.add_node(state_node)
                    eid_hash = '(' + op_node.get_name()  + "," + state_node.get_name()  + ')'
                    backward_hash = '(' + state_node.get_name() + "," + op_node.get_name()   + ')'
                    if eid_hash not in pairs:
                        pydot_graph.add_edge(pydot.Edge(op_node, state_node))
                        pydot_graph.add_edge(pydot.Edge(state_node, op_node))
                        pairs.append(eid_hash)
                        pairs.append(backward_hash)
                    if graph.edge_info[s].iid and graph.edge_info[s].vid:
                        vid = graph.edge_info[s].vid
                        if vid in graph.output:
                            name = graph.edge_info[vid].name
                            vid_node = edge_ids[name]

                            eid_hash = '(' + state_node.get_name() + "," + vid_node.get_name() + ')'
                            backward_hash = '(' + vid_node.get_name() + "," + state_node.get_name() + ')'
                            if eid_hash not in pairs:
                                pydot_graph.add_edge(pydot.Edge(state_node, vid_node))
                                pairs.append(eid_hash)
                                pairs.append(backward_hash)

    return pydot_graph



# A dummy minimal PNG image used by GetGraphPngSafe as a
# placeholder when rendering fail to run.
_DummyPngImage = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00'
    b'\x01\x01\x00\x00\x00\x007n\xf9$\x00\x00\x00\nIDATx\x9cc`\x00\x00'
    b'\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82')


def GetGraphPngSafe(func, *args, **kwargs):
    """
    Invokes `func` (e.g. GetPydotGraph) with args. If anything fails - returns
    and empty image instead of throwing Exception
    """
    try:
        graph = func(*args, **kwargs)
        if not isinstance(graph, pydot.Dot):
            raise ValueError("func is expected to return pydot.Dot")
        return graph.create_png()
    except Exception as e:
        logger.error("Failed to draw graph: {}".format(e))
        return _DummyPngImage


def visualize_program(input_proto, rankdir="LR"):
    program = load_store.load_program(input_proto)
    graph = program.graph
    pydot_graph = pydot.Dot(name=program.name, rankdir=rankdir)
    output_dir, output_file = os.path.split(input_proto)

    out_graph = GetPydotGraph(graph,name=graph.name,rankdir=rankdir)
    filename = output_dir + '/' + output_file[:-3] + '.dot'
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
