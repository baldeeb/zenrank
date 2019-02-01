from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from decimal import *
from nodeTools import Node


# from nltk.corpus import wordnet
# from nltk.corpus import wordnet as wn

def getWeight(keyTerm, searchTerms, merge = "or"):
    if merge == "and": 
        score = Decimal(1)
        for searchTerm in searchTerms:
            newScore = Decimal(fuzz.partial_ratio(keyTerm.lower().strip("_"), searchTerm.lower().strip("_"))) / Decimal(100)
            score = score * newScore
        return score * 100
    
    elif merge == "or":
        score = 0
        for searchTerm in searchTerms:
            score = max(score, fuzz.partial_ratio(keyTerm.lower().strip("_"), searchTerm.lower().strip("_")))
        return score
    
    # elif merge == "WordNet":
    #     score = 0
    #     for searchTerm in searchTerms:

    #         score = max(score, )
        
def cleanSearchSet(searchSet):
    newSearchSet = set()
    for sword in searchSet:
        if len(sword) > 2: 
            newSearchSet.add(sword) 
    return newSearchSet

def matchKeyWordsToSearchWords(kwDict, swSet, verbose = False):
    swSet = cleanSearchSet(swSet)

    for kw, kwNode in kwDict.items():
        kwNode.weight = getWeight(kw, swSet, "and")

        if verbose is True:
            print("Key Word \"" + kw + "\" has score: " + str(kwNode.weight))

if __name__=="__main__":
    keywords = {
        "Distance"          : Node("node1"), 
        "dist"              : Node("node2"), 
        "distance"          : Node("node3"),
        "pythagorous"       : Node("node4"), 
        "pyth"              : Node("node5"),
        "triangle"          : Node("node6"),
        "apple"             : Node("node7"),
        "add"               : Node("node8"),
        "dist_Pythagorous"  : Node("node9")
    }
    searchwords = {"distance", "Pythagorous", "D"}

    matchKeyWordsToSearchWords(keywords, searchwords)