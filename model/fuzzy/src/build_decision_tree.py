import math
from get_data import get_fuzzy_dict
from fuzzy.FuzzyElement import FuzzyElement
from fuzzy.FuzzyDecisionNode import FuzzyDecisionNode
import pandas as pd

fuzzyDict = get_fuzzy_dict()

# , 0.05 , -0.00001, 0.32
yc = FuzzyDecisionNode(FuzzyElement(fuzzyDict["yellowCards"]))
# , 0.03, 0.09, -0.063
rc = FuzzyDecisionNode(FuzzyElement(fuzzyDict["redCards"]))
# , 33, -0.062, -0.184
p = FuzzyDecisionNode(FuzzyElement(fuzzyDict["points"]))
#, 4.71
pos = FuzzyDecisionNode(FuzzyElement(fuzzyDict["possession"]), rc, p)
#, 9
p = FuzzyDecisionNode(FuzzyElement(fuzzyDict["points"]), yc, pos)
root = FuzzyDecisionNode(FuzzyElement(fuzzyDict["goals"]), yes_node=None, no_node=p)

standings = pd.read_json('./../../data-generation/out/training_data/diff-2022-2023.json')

accuracy, count = 0, 0


for _, row in standings.iterrows():
    count += 1
    standing = row.to_dict()
    # evaluate returns a score from 0 to 1, so we multiply to get the actual outcome encodings:
    # 0 - loss, 1 - draw, 2 - win
    predict = root.evaluate(standing) * 2

    print(predict, standing["matchOutcome"], standing["team_one_name"], standing["team_two_name"])
    if round(predict) == standing["matchOutcome"]:
        accuracy += 1

accuracy /= count

print(f'Accuracy {accuracy}')

