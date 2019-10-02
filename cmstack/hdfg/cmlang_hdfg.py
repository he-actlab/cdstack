from cmstack.hdfg.hdfg_pb2 import Component, Program
from cmstack.hdfg.hdfgutils import make_attribute, get_attribute_value, make_edge_info, make_node, make_statement_graphs
import logging

def map_args(instance_args, arg_dict, edges):
    new_args = {'inputs' : [],
                'outputs': [],
                'params' : [],
                'states' : []}
    for a in range(len(arg_dict['args'])):
        if a == len(instance_args):
            break
        arg = arg_dict['args'][a]
        if arg in arg_dict['input']:
            new_args['inputs'].append(instance_args[a])
        elif arg in arg_dict['output']:
            new_args['outputs'].append(instance_args[a])
        elif arg in arg_dict['state']:
            new_args['states'].append(instance_args[a])
        elif arg in arg_dict['param']:
            new_args['params'].append(instance_args[a])

    for p in arg_dict['args'][len(instance_args):]:
        if 'default' not in edges[p].keys():
            logging.error(f"Parameter without default value unspecified {p}")
        else:
            new_args['params'].append(p)
    return new_args

def create_hdfg(components, outfile):
    for t in components.keys():
        for n in components[t]['statements']:
            if components[t]['nodes'][n]['op_cat'] == 'component':
                cname = components[t]['nodes'][n]['op']
                sig = components[cname]['signature']
                instance_args = components[t]['nodes'][n]['inputs']
                components[t]['nodes'][n]['ordered_args'] = instance_args
                new_args = map_args(instance_args, sig, components[cname]['edges'])
                components[t]['nodes'][n]['inputs'] = new_args['inputs']
                components[t]['nodes'][n]['outputs'] = new_args['outputs']
                components[t]['nodes'][n]['states'] = new_args['states']
                components[t]['nodes'][n]['params'] = new_args['params']
                for o in new_args['outputs']:
                    components[t]['edges'][o]['src'] = [n]

    return cmlang_proto(components, outfile)




def generate_template(template, node_info, edge_info, nodes, sinputs):
    proto_nodes = []
    for n in nodes:
        proto_nodes.append(make_node(n,
                        node_info[n]['op'],
                        **node_info[n]))
    template.sub_graph.extend(proto_nodes)

    for edge_name, edge in edge_info.items():
        proto_edge = make_edge_info(edge_name,**edge)
        template.edge_info[edge_name].CopyFrom(proto_edge)

    statements = []
    for s in sinputs:
        statement_component = Component(name=s['name'],
                                        op_type=s['statement_type'],
                                        op_cat=node_info[s['nodes'][0]]['op_cat'])
        statement_component.input.extend(s['inputs'])
        statement_component.output.extend(s['outputs'])
        snodes = []
        for n in s['nodes']:
            snodes.append(make_node(n,
                                         node_info[n]['op'],
                                         **node_info[n]))
        statement_component.sub_graph.extend(snodes)
        statements.append(statement_component)

    template.statements.extend(statements)

def cmlang_proto(components, name):
    program = Program(name=name)
    templates = program.templates
    sep = "/"
    edge_attr = make_attribute('edges', 0)
    program.attributes['edges'].CopyFrom(edge_attr)
    component_attr = make_attribute('components', 0)
    program.attributes['components'].CopyFrom(component_attr)

    for name,comp in components.items():
        template = Component(name=name, op_type=comp['op_type'])
        template.input.extend(comp['signature']['input'])
        template.output.extend(comp['signature']['output'])
        template.state.extend(comp['signature']['state'])
        template.parameters.extend(comp['signature']['param'])
        template.domains.extend(comp['domains'])
        template.assumptions = comp['assumptions']
        template.instructions.extend(comp['instructions'])

        template.attributes['ordered_args'].CopyFrom(make_attribute('ordered_args',
                                                                    comp['signature']['args']))
        template.attributes['statements'].CopyFrom(make_attribute('statements',
                                                                    comp['executions']))
        template.statement_graphs.extend(make_statement_graphs(comp['statement_graphs']))
        generate_template(template, comp['nodes'], comp['edges'], comp['statements'], comp['statement_inputs'])
        templates[name].CopyFrom(template)

    def hdfg_proto(graph,template_name, scope, inst_args):

        graph.name = scope

        edge_info = templates[template_name].edge_info

        edges = get_attribute_value(program.attributes['edges'])
        components = get_attribute_value(program.attributes['components'])

        t_inputs = templates[template_name].input
        t_outputs = templates[template_name].output
        t_states = templates[template_name].state
        t_params = templates[template_name].parameters
        args = get_attribute_value(templates[template_name].attributes['ordered_args'])
        for e in edge_info:


            if e in args:
                idx = args.index(e)
                if (len(inst_args) - 1) < idx:
                    edge_name = scope + sep + e
                    graph.edge_info[e].CopyFrom(edge_info[e])
                    graph.edge_info[e].name = edge_name
                    graph.edge_info[e].gid = edges
                    edges += 1
                else:
                    graph.edge_info[e].CopyFrom(inst_args[idx])
            else:
                edge_name = scope + sep + e
                graph.edge_info[e].CopyFrom(edge_info[e])
                graph.edge_info[e].name = edge_name
                graph.edge_info[e].gid = edges
                edges += 1
        # graph.input.extend(t_inputs)
        # graph.output.extend(t_outputs)
        # graph.state.extend(t_states)
        # graph.parameters.extend(t_params)

        edge_attr = make_attribute('edges', edges)
        program.attributes['edges'].CopyFrom(edge_attr)

        for n in templates[template_name].sub_graph:
            node_type = n.op_cat
            new_node = Component()
            new_name = scope + sep + n.name
            components += 1
            if node_type == 'component':
                component_attr = make_attribute('components', components)
                program.attributes['components'].CopyFrom(component_attr)
                node_arg_names = get_attribute_value(n.attributes['ordered_args'])
                node_args = []
                for node_arg in node_arg_names:
                    node_args.append(graph.edge_info[node_arg])

                hdfg_proto(new_node,n.op_type, new_name,node_args)
                components = get_attribute_value(program.attributes['components'])
                for key in n.attributes:
                    new_node.attributes[key].CopyFrom(n.attributes[key])
                new_node.input.extend(n.input)
                new_node.output.extend(n.output)
                new_node.state.extend(n.state)
                new_node.parameters.extend(n.parameters)
                new_node.op_type = n.op_type
                new_node.op_cat = n.op_cat

            else:
                new_node.CopyFrom(n)
            new_node.name = new_name
            new_node.gid = components - 1
            graph.sub_graph.extend([new_node])
        component_attr = make_attribute('components', components)
        program.attributes['components'].CopyFrom(component_attr)

    graph = Component(name='main', op_type='component')
    hdfg_proto(graph, 'main', 'main', [])

    added_input = False
    outputs = []
    for n in graph.sub_graph:
        op_cat = n.op_cat
        if op_cat == 'component':
            ctype = program.templates[n.op_type].op_type
            if not added_input:
                graph.input.extend(list(n.input))
                added_input = True
            graph.state.extend(list(n.state))
            if ctype == 'reservoir':
                outputs = list(n.input)
            else:
                outputs = list(n.output)

    graph.output.extend(outputs)
    program.graph.CopyFrom(graph)
    return program