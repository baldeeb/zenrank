keywordDict = {}

class Edge(object):
    def __init__(self, node, weight = 1):
        self.weight = weight
        self.node = node

class Node(object):
    def __init__(self, name, weight = 0):
        self.weight = weight
        self.name = name
        self.edges = []

    def connect(self, node, edgeWeight):
        self.edges.append(Edge(node, edgeWeight))

def connectKeywordsToNode(keywords, counts, node):
    createdNodes = []
    for entry in zip(keywords, counts):
        newNode = Node(entry[0])   # create new node for every keyword
        keywordDict.append({entry[0]: newNode})
        newNode.connect(node, entry[1])  # connect keyword to method and assign count as edge weight
        createdNodes.append(newNode)
    return createdNodes

def connectListToNode(names, node):
    createdNodes = []
    edgeWeight = 1 / len(names)
    for name in names:
        newNode = Node(name)
        newNode.connect(node, edgeWeight)
        createdNodes.append(newNode)
    return createdNodes



if __name__=="__main__":
    
