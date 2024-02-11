import pandas as pd

from FuzzyElement import FuzzyElement
from pprint import pprint

# display one team's fitness as product of its μ fields
# 1. teams json
# 2. μ calculator
# 3. predict outcomes via diff in fit(team) vs actual outcomes 

df = pd.read_json('../../data-generation/out/training_data/teams-2022-2023.json')
thresholds = pd.read_json('./thresholds.json')

teams = []
for index, row in df.iterrows():
    team = {"stats": []}
    for col in df.columns:
        params_row = thresholds.loc[thresholds['name'] == col]
        if params_row.empty:
            team[col] = row[col]
            continue
        x = params_row['params']

        a = x.values[0]['a']
        b = x.values[0]['b']
        type = params_row['type'].iloc[0]
        element = FuzzyElement(col, type, row[col], a, b)
        team['stats'].append(element)
    teams.append(team)


scores = {}
for team in teams:
    team_score = 0
    for stat in team["stats"]:
        team_score += stat.mu
    scores[team["name"]] =  team_score

print(scores)

outcomes = pd.read_json('../../data-generation/out/training_data/sample-2022-2023.json')

accuracy, count = 0, 0
for i in outcomes.index:
    count += 1
    outcome = outcomes['matchOutcome'][i]
    team_one_name = outcomes['team_one_name'][i]
    team_two_name = outcomes['team_two_name'][i]
    fit_one, fit_two = scores[team_one_name], scores[team_two_name]
    predict = 1
    if fit_one - fit_two > 0.4:
        predict = 2
    if fit_two - fit_one > 0.4:
        predict = 0
    
    if predict == outcome:
        accuracy += 1

accuracy /= count

print(accuracy)
