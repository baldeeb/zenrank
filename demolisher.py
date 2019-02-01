def resetWeightHelper(node):
    for edge in node.edges:
        resetWeight(edge.node)

def resetWeight(node):
    for edge in node.edges:
        edge.weight = 1
        resetWeight(edge.node)
    node.weight = 0

def resetGraphWeights(kwDict):
    for kw, kwNode in kwDict.items():
        resetWeightHelper(kwNode)
