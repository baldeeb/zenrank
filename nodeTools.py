from decimal import *

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
        self.baseWeight = 1

    def connect(self, node, edgeWeight):
        self.edges.append(Edge(node, edgeWeight))

def connectKeywordsToNode(keywordCountDict, node):
    createdNodes = []
    for kw, count in keywordCountDict.items():
        if kw in keywordDict.keys():
            newNode = keywordDict[kw]
        else:
            newNode = Node(kw)   # create new node for every keyword
            keywordDict[kw] = newNode
            createdNodes.append(newNode)
        
        newNode.connect(node, count)  # connect keyword to method and assign count as edge weight
    return createdNodes

def connectListToNode(names, node):
    createdNodes = []
    edgeWeight = Decimal(1) / Decimal(len(names))
    for name in names:
        newNode = Node(name)
        newNode.connect(node, edgeWeight)
        createdNodes.append(newNode)
    return createdNodes





def printGraph(kwDict):
    for kw, kwNode in kwDict.items():
        print("kw: " + kw + " -- " + str(kwNode.weight))
        for kwEdge in kwNode.edges:
            print("    -" + str(kwEdge.weight) + "--> " + kwEdge.node.name)
            for childEdge in kwEdge.node.edges:
                print("        -" + str(childEdge.weight) + "--> " + childEdge.node.name)
                for infantEdge in childEdge.node.edges:
                    print("            -" + str(infantEdge.weight) + "--> " + infantEdge.node.name)
                    if len(infantEdge.node.edges):
                        "      Infant has edges..."


if __name__=="__main__":
    repo = { "class1": {
                        "m0":{
                                "distance": 2 , 
                                "Add": 1
                            } ,
                        "m1":{
                                "distance": 1, 
                                "get": 2
                            }
                        } ,
             "class2": 
                        {"m2":{
                                "ParticleFilter": 1
                              }
                        },
             "class3": 
                        {"m3,":{
                                "convertUnit": 1
                                }
                        },
             "class4": 
                        {"m4":{
                               "static": 3
                              }
                        }
            }

    repoNodes = Node("repo",0)
    
    classNodes = connectListToNode(repo.keys(),repoNodes) 
      
    for node in classNodes:
        nodeDict = repo[node.name]
        methodsNodes = connectListToNode(nodeDict.keys(), node)
        
        for method in methodsNodes:
            methodDict = nodeDict[method.name]             
            keywordNodes = connectKeywordsToNode(methodDict, method)

    printGraph(keywordDict)
        







    
