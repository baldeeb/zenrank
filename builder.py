from nodeTools import *
from ranker import rankGraph


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
        methodsNodes = connectListToNode( repo[node.name].keys(), node)
        for method in methodsNodes:            
            mm = connectKeywordsToNode(repo[node.name][method.name].keys(), repo[node.name][method.name].values(), method)

    rankGraph(keywordDict)
    printGraph(keywordDict)
