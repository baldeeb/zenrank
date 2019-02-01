import Queue

def updateWeightHelper(node):
    for edge in node.connections:
        updateWeight(edge.node, node.weight * edge.weight)

def updateWeight(node, parentWeight):
    for edge in node.connections:
        updateWeight(edge.node, node.baseWeight * edge.weight * parentWeight)
    node.weight = node.weight * edge.weight * parentWeight

def rankGraph(kwDict):
    for kw, kwNode in kwDict.items():
        updateWeightHelper(kwNode)
