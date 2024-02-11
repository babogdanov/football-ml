import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_json('../../data-generation/out/training_data/teams-2022-2023.json')

#print(df['team_two_points'])
#plt.hist(df['team_one_points'].tolist())
while(True):
    col = input("Enter column name: ")
    if col not in df.columns:
        print('No such column!')
        continue
    plt.hist(df[col].tolist())
    plt.show() 
    
    
