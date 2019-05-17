import json


class DFGNode:
    def __init__(self):
        self.id = None
        self.operation = None
        self.children = []  # order doesn't matter
        self.parents = []  # order matters
        self.dist2sink = None
        self.dataType = None  # e.g. model_input, gradient, etc.

    def toDict(self):
        childrenIDs = []
        parentsIDs = []
        for child in self.children:
            childrenIDs.append(child.id)
        for parent in self.parents:
            parentsIDs.append(parent.id)
        return {'id': self.id, 'operation': self.operation, 'children': childrenIDs, 'parents': parentsIDs,
                'dist2sink': self.dist2sink, 'dataType': self.dataType}

    def __str__(self):
        return json.dumps(self.toDict(), sort_keys=True, indent=2)

    def insertParent(self, int, val):
        self.parents.insert(int, val)

    def fromDict(self, d):
        self.id = d['id']
        self.operation = d['operation']
        self.children = d['children']
        self.parents = d['parents']
        self.dist2sink = d['dist2sink']
        self.dataType = d['dataType']

    def fromStr(self, s):
        self.fromDict(json.loads(s))

    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.__str__())

    def load(self, path):
        with open(path, 'r') as f:
            self.fromStr(f.read())


class DataFlowGraph:

    def __init__(self):
        self.nodes = []

    def __copy__(self):
        copy = DataFlowGraph()
        copy.nodes = self.nodes.copy()
        return copy

    def add(self, node):
        self.nodes.append(node)

    def get(self, index):
        return self.nodes[index]

    def remove(self, node):
        self.nodes.remove(node)

    def isEmpty(self):
        return len(self.nodes) == 0

    def updateId(self):
        for i in range(len(self.nodes)):
            self.nodes[i].id = i

    '''
    def toDict(self):
        d = {}
        for node in self.nodes:
            id = node.id
            d[id] = node.toDict()

        for key in self.nodes:
            dfgNode = self.nodes[key]
            d[key] = dfgNode.toDict()

        return d
    '''

    def toList(self):
        list = []
        for node in self.nodes:
            list.append(node.toDict())
        return list

    def __str__(self):
        return json.dumps(self.toList(), sort_keys=True, indent=2)

    '''
    def fromDict(self, d):

        dfg = self.__init__()
        for nodeKey in d.keys():
            node = d[nodeKey]
            newNode = DFGnode()
            newNode.fromDict(node)
            dfg.add(newNode)

        pass
    '''

    def fromList(self, l):
        for nodeDict in l:
            node = DFGNode()
            node.fromDict(nodeDict)
            self.add(node)

    def fromStr(self, s):
        self.fromList(json.loads(s))

    def getSize(self):
        return len(self.nodes)

    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.__str__())

    def load(self, path):
        with open(path, 'r') as f:
            self.fromStr(f.read())
