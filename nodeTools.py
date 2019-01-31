keywordDict = {}

class Edge(object):
    
    def __init__(self, node, weight = 1):
        self.weight = weight
        self.node = node

class Node(object):

    def __init__(self, name, isKeyword = False, weight = 0):
        if isKeyword:
            keywordDict.append({name: self})
        self.weight = weight
        self.name = name
        self.edges = []

    def connect(self, node, edgeWeight):
        self.edges.append(Edge(node, edgeWeight))

def connectKeywordsToMethod(keywords, counts, node):
    createdNodes = []
    for entry in zip(keywords, counts):
        newNode = Node(entry[0], True)   # create new node for every keyword
        newNode.connect(node, entry[1])  # connect keyword to method and assign count as edge weight
        createdNodes.append(newNode)
    return createdNodes

def connectMedthodsToClass(methodNames, classNode):
    edgeWeight = 1 / len(methodNames)
    for name in methodNames:
        newNode = Node(name)
        newNode.connect(classNode, edgeWeight)

def connectClassesToRepo(classNames, repoNode):
    edgeWeight = 1 / len(classNames)
    for name in classNames:
        newNode = Node(name)
        newNode.connect(repoNode, edgeWeight)


