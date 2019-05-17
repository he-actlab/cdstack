from graphviz import Digraph
import hdfg_pb2 as hdfg


class HDFG:

    def __init__(self, graph):
        assert 'main' in graph.component_definitions, "Error! Main component required"
        self.graph = graph
        self.definitions = graph.component_definitions
        self.instance_counts = {}
        self.instance_counts['main'] = 1
        self.cid = 0
        self.parent_cid = 0
        self.parent_cdef_name = ''
        main_component = hdfg.Component(cid=self.cid,
                                          cdef=self.graph.component_definitions['main'])
        self.cid += 1
        self.traverse_graph(main_component)

    def traverse_graph(self, component):
        print(component.cdef.cname)
        for cid in component.cdef.sub_component_ids:
            sub_graph = component.sub_components.add(cid=self.cid, cdef=self.graph.component_definitions[cid])
            self.cid += 1
            if not component.cdef.sub_components[cid].is_op:
                print("Component: {}, Args: {}".format(cid, component.cdef.sub_components[cid].ordered_args))
                for eid in component.cdef.sub_components[cid].ordered_args:
                    break

                self.traverse_graph(sub_graph)
            # self.make_component()

    ## Requires assigning unique ids to inputs, outputs, states, params, sub_edges
    ## sub_components, and predicate_id. Lastly assigns component definition
    def make_component(self, component):
        pass


    ## Requires assigning unique ids to local_src, local_dst, dimension values, predicate_ids,
    ## and globally unique id to itself. Lastly assigns edgeinfo and actual data
    def make_edge(self, edge):
        pass

        # self.graph.components.add([new_node])

    def handle_declarations(self, declarations):
        pass

    def create_graphviz(self):
        pass
        # cluster_name = 'cluster' + str(self.instance_counts[parent])
        # label_name = parent + '$' + str(self.instance_counts[parent])
        # with self.G.subgraph(name=cluster_name) as g:
        #     g.attr(label=label_name)
        #         g.node(eid)





