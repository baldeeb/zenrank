def updateWeightHelper(node):
    for edge in node.edges:
        # print(node.name + " --> " + edge.node.name + "")
        updateWeight(edge.node, node.weight * edge.weight)

def updateWeight(node, parentWeight):
    for edge in node.edges:
        # print(node.name + " --> " + edge.node.name + "")
        updateWeight(edge.node, node.baseWeight * edge.weight * parentWeight)
    # print("> " + node.name + " <")
    node.weight = node.weight + (node.baseWeight * parentWeight)

def rankGraph(kwDict):
    for kw, kwNode in kwDict.items():
        updateWeightHelper(kwNode)
