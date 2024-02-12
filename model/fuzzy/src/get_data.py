import math
from numpy import Infinity
import pandas as pd

from fuzzy.FuzzyElement import FuzzyElement


# display one team's fitness as product of its μ fields
# 1. teams json
# 2. μ calculator
# 3. predict outcomes via diff in fit(team) vs actual outcomes


def get_teams():
    df = pd.read_json(
        '../../data-generation/out/training_data/teams-2022-2023.json')
    thresholds = pd.read_json('./thresholds/single_team.json')

    teams = []
    for _, row in df.iterrows():
        team = {"stats": []}
        for col in df.columns:
            params_row = thresholds.loc[thresholds['name'] == col]
            if params_row.empty:
                team[col] = row[col]
                continue
            params = params_row.to_dict(orient='records')[0]
            element = FuzzyElement(params, row[col])
            team['stats'].append(element)
        teams.append(team)
    return teams

def get_fuzzy_dict(type='diff'):
    if type not in ['diff', 'single']:
        raise Exception('unsupported treshold')
    file = 'diff' if type == 'diff' else 'single_team'
   # print(type, file)
    thresholds = pd.read_json('./thresholds/' + file + '.json')
    fuzzy_dict = {}
    for i in thresholds.index:
        fuzzy_dict[thresholds['name'][i]] = {"name": thresholds["name"][i], "type": thresholds["type"][i], "params": thresholds["params"][i]}
    return fuzzy_dict
