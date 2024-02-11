import pandas as pd

from FuzzyElement import FuzzyElement
from pprint import pprint

# display one team's fitness as product of its μ fields
# 1. teams json
# 2. μ calculator
# 3. predict outcomes via fit(team)

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


scores = []
for team in teams:
    team_score = 0
    for stat in team["stats"]:
        team_score += stat.mu
    scores.append((team["name"], team_score))

print(scores)