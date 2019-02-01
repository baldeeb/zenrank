from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from decimal import *
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
        


if __name__=="__main__":
    keywords = {
                    "Distance", "dist", "distance",
                    "pythagorous", "pyth", "triangle", 
                    "apple", "add", "dist_Pythagorous"
                }
    searchwords = {"distance", "Pythagorous", "D"}

    newSearchWords = set()
    for sword in searchwords:
        if len(sword) > 2: 
            newSearchWords.add(sword) 

    for kword in keywords:
        score = getWeight(kword, newSearchWords, "and")
        print("    key word \"" + kword + "\" has score: " + str(score))