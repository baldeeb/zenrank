from nodeTools import *
from ranker import rankGraph
from matcher import matchKeyWordsToSearchWords

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

    repoNodes = Node("repo",0)
    
    classNodes = connectListToNode(repo.keys(),repoNodes) 
      
    for node in classNodes:
        nodeDict = repo[node.name]
        methodsNodes = connectListToNode(nodeDict.keys(), node)
        
        for method in methodsNodes:
            methodDict = nodeDict[method.name]             
            keywordNodes = connectKeywordsToNode(methodDict, method)

    printGraph(keywordDict)

    print()
    print("Re-weighing graph...")
    print()
        
    # re-weigh
    matchKeyWordsToSearchWords(keywordDict, searchwords)
    rankGraph(keywordDict)

    printGraph(keywordDict)
