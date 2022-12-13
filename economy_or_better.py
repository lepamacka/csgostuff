import os, glob, json
import numpy as np
from awpy.parser import DemoParser

estapath = './esta-main/data/lan'

matchstats_list = []
N = 0
for filename in glob.glob(os.path.join(estapath, '*.json')):
    parser = DemoParser()
    data=parser.read_json(filename)
    matchstats = {"rounds": []}
    matchstats["matchwinner"] = None
    print(N)
    N+=1
    for r in data["gameRounds"]:
        roundstats = {"winningTeam": r["winningTeam"], "winningSide": r["winningSide"]}

        ctmaxval = 0.
        tmaxval = 0.
        for f in r["frames"]:
            if ctmaxval < f['ct']['teamEqVal'] and (f["seconds"] < 20. and not f["bombPlanted"]): #NOT a good way of doing it.
                ctmaxval = f['ct']['teamEqVal']
            if tmaxval < f['t']['teamEqVal'] and (f["seconds"] < 20. and not f["bombPlanted"]): #NOT a good way of doing it.
                tmaxval = f['t']['teamEqVal']
        roundstats["CTeconomy"] = ctmaxval
        roundstats["Teconomy"] = tmaxval


        if ((r["endTScore"] == 16 and r["endCTScore"] < 15) or (
        r["endTScore"] == 19 and r["endCTScore"] < 18)) or ((
        r["endTScore"] == 22 and r["endCTScore"] < 21) or (
        r["endTScore"] == 25 and r["endCTScore"] < 24)):
            matchstats["matchwinner"] = r["tSide"]["teamName"]

        elif ((r["endCTScore"] == 16 and r["endTScore"] < 15) or (
        r["endCTScore"] == 19 and r["endTScore"] < 18)) or ((
        r["endCTScore"] == 22 and r["endTScore"] < 21) or (
        r["endCTScore"] == 25 and r["endTScore"] < 24)):
            matchstats["matchwinner"] = r["ctSide"]["teamName"]

        matchstats["rounds"].append(roundstats)

    matchstats_list.append(matchstats)

json.dump(matchstats_list, open("economywin_data.json", 'w'))
