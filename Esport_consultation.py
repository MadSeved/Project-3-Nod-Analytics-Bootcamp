import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import time

df=pd.read_csv("datadump_s5-000.csv")
df = df.loc[df.platform == "PC"]
df = df.loc[df.skillrank == "Diamond"]
df.drop(columns = ["objectivelocation", "roundduration", "clearancelevel", 'primaryweapon', 'primaryweapontype', 'primarysight', 'primarygrip', 'primaryunderbarrel', 'primarybarrel', 'secondaryweapon', 'secondaryweapontype', 'secondarysight', 'secondarygrip', 'secondaryunderbarrel', 'secondarybarrel', 'secondarygadget'], inplace=True)
x=1
for i in range(1,10):
    print(x)
    temp_df = pd.read_csv(f"datadump_s5-00{i}.csv")
    temp_df = temp_df.loc[temp_df.platform == "PC"]
    temp_df = temp_df.loc[temp_df.skillrank == "Diamond"]
    temp_df.drop(columns = ["objectivelocation", "roundduration", "clearancelevel", 'primaryweapon', 'primaryweapontype', 'primarysight', 'primarygrip', 'primaryunderbarrel', 'primarybarrel', 'secondaryweapon', 'secondaryweapontype', 'secondarysight', 'secondarygrip', 'secondaryunderbarrel', 'secondarybarrel', 'secondarygadget'], inplace=True)
    df = pd.concat([df, temp_df])
    x+=1

for i in range(10, 22):
    print(x)
    temp_df = pd.read_csv(f"datadump_s5-0{i}.csv")
    temp_df = temp_df.loc[temp_df.platform == "PC"]
    temp_df = temp_df.loc[temp_df.skillrank == "Diamond"]
    temp_df.drop(columns = ["objectivelocation", "roundduration", "clearancelevel", 'primaryweapon', 'primaryweapontype', 'primarysight', 'primarygrip', 'primaryunderbarrel', 'primarybarrel', 'secondaryweapon', 'secondaryweapontype', 'secondarysight', 'secondarygrip', 'secondaryunderbarrel', 'secondarybarrel', 'secondarygadget'], inplace=True)
    df = pd.concat([df, temp_df])
    x+=1
operator_lst=["SPETSNAZ-RESERVE",'SAS-RESERVE','GIGN-RESERVE','GSG9-RESERVE','SWAT-RESERVE']
for i in operator_lst:
    df.drop(list(df.loc[df.operator == i].index), inplace=True)
df.reset_index(inplace=True)
df.drop(columns= "index", inplace=True)

a_frame = df.groupby(["matchid", "haswon"])["haswon"].count().to_frame().unstack()
a_frame.fillna(0, inplace=True)
a_lst = []
for i in range(len(a_frame)):
    if a_frame.iloc[i, 0] < a_frame.iloc[i, 1]:
        a_lst.append("match win")
    elif a_frame.iloc[i, 0] > a_frame.iloc[i, 1]:
        a_lst.append("match loss")
    else:
        a_lst.append("match draw")
a_frame["match_result"] = a_lst
index_a_frame = list(a_frame.index)

df["match_result"] = "match loss"

x=0
for i in index_a_frame:
    temp_lst = list(df.match_result.loc[df.matchid == i].index)
    df.match_result.iloc._setitem_with_indexer(temp_lst, a_lst[x])
    x+=1
    
b_frame = df.groupby("operator", as_index=False).mean()[["operator", "haswon"]]
df["op_round_winrate"] = 0

for i in range(len(df)):
    x=0
    for j in list(b_frame.operator):
        if df.loc[i, "operator"] == j:
            df.loc[i, "op_round_winrate"] = b_frame.haswon[x]
        x+=1