from nodeTools import *
from ranker import rankGraph
from matcher import matchKeyWordsToSearchWords


def collectResults(kwDict):
    for kw, kwNode in kwDict.items():
        collectChildrenResult(kwNode)

    return sorted(resultsDict.items(), key=lambda x:x[1])

def collectChildrenResult(node):
    for edge in node.edges:
        if edge.node.name not in resultsDict:
            resultsDict[edge.node.name] = edge.node.weight
        collectChildrenResult(edge.node)




if __name__=="__main__":
    repo = { 
        "class1": {
            "m0":{
                "distance": 2 , 
                "Add": 1
            } ,
            "m1":{
                "distance": 1, 
                "get": 2
            }
        } ,
        "class2":{
            "m2":{
                "ParticleFilter": 1
            }
        },
        "class3":{
            "m3,":{
                "convertUnit": 1
            }
        },
        "class4":{
            "m4":{
                "static": 3
            }
        }
    }


    searchwords = {"distance", "Pythagorous", "D"}

    # Construct graph

    repoNodes = Node("repo")
    
    classNodes = connectListToNode(repo.keys(),repoNodes) 
      
    for node in classNodes:
        nodeDict = repo[node.name]
        methodsNodes = connectListToNode(nodeDict.keys(), node)
        
        for method in methodsNodes:
            methodDict = nodeDict[method.name]             
            keywordNodes = connectKeywordsToNode(methodDict, method)

    # printGraph(keywordDict)
    # print()

    print("Re-weighing graph...")
    
        
    # re-weigh
    matchKeyWordsToSearchWords(keywordDict, searchwords, verbose = True)
    rankGraph(keywordDict)

    # printGraph(keywordDict)

    results = collectResults(keywordDict)

    for (key, value) in results:
        print( "Word: " + key + ", Rank: " + str(value))