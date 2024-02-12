
import math
import pandas as pd

from get_data import get_teams


teams = get_teams()
scores = {}
for team in teams:
    team_score = pow(10, 6)
    for stat in team["stats"]:
        if stat.get_mu() == 0 or not stat.get_mu():
            print(stat.name, team["name"])
        team_score *= stat.get_mu()

    scores[team["name"]] = math.log2(team_score)

print(scores)

outcomes = pd.read_json(
    '../../data-generation/out/training_data/sample-2022-2023.json')

accuracy, count = 0, 0
diff_threshold = 0
for i in outcomes.index:
    count += 1
    outcome = outcomes['matchOutcome'][i]
    team_one_name = outcomes['team_one_name'][i]
    team_two_name = outcomes['team_two_name'][i]
    fit_one, fit_two = scores[team_one_name], scores[team_two_name]
    predict = 1
    if fit_one - fit_two > diff_threshold:
        predict = 2
    if fit_two - fit_one > diff_threshold:
        predict = 0

    if predict == outcome:
        accuracy += 1
accuracy /= count

print(accuracy)

# 31 draws, 159 wins/draws
# 0.1631578947368421 accuracy if we always assume draw
# 0.42 accuracy if we assume win/loss at random
# 0.5894736842105263 accuracy if we always assume better fit wins where fit=log(product of mu) and no special weights for any value of mu; for any threshold > 0 results get worse
