import hdfg.hdfg_pb2 as hdfg_pb2

def test():
    graph = hdfg_pb2.Node()
    graph.name = 'main'

    A = hdfg_pb2.Node()
    A.name = 'A'

    B = hdfg_pb2.Node()
    B.name = 'B'


    A_out = hdfg_pb2.Edge()
    A_out.name = 'A1'
    A_out.dims.append(1)
    A_out.dims.append(3)
    A_out.source = A.name
    A_out.target = B.name

    A.output.extend([A_out])

if __name__ == '__main__':
    test()


