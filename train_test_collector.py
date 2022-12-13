import os, glob, json
import numpy as np
from awpy.parser import DemoParser

train_list = []
test_list = []
estapath = './esta-main/data/lan'
N = 0
for filename in glob.glob(os.path.join(estapath, '*.json')):
    parser = DemoParser()
    data=parser.read_json(filename)
    tickrate = float(data["tickRate"])
    print(N)
    N+=1
    for r in data["gameRounds"]:
        firstdamage = {"tick": 9999999999}
        for d in r["damages"]:
            if (d["attackerSide"] != d["victimSide"] and d["attackerSide"]):
                if d["tick"] < firstdamage["tick"] and d["weaponClass"] != "Grenade":
                    firstdamage = d.copy()
        if firstdamage["tick"] < 9999999999:
            #xangoff = (firstdamage["attackerViewX"] + 540. - firstdamage["victimViewX"])%360.
            xangoff = (180./np.pi * np.arccos((firstdamage["victimX"] - firstdamage["attackerX"])/np.linalg.norm([firstdamage["victimX"] - firstdamage["attackerX"], firstdamage["victimY"] - firstdamage["attackerY"]])) * np.sign(firstdamage["victimY"] - firstdamage["attackerY"]) + 540. - firstdamage["victimViewX"])%360.
            if xangoff > 180.:
                xangoff = xangoff - 360.
            firstdamage["xAngleOffsetFirstDamage"] = xangoff
        tmaxval = 0.
        ctmaxval = 0.
        properlen = 26
        for f in r["frames"]:
            framevars = [f['seconds']]
            if f['bombPlanted']:
                framevars.append(1)
            else:
                framevars.append(0)
            framevars += [0]*12
            if not (f['ct']['alivePlayers'] > 5 or f['t']['alivePlayers'] > 5):
                framevars[f['ct']['alivePlayers']+2] = 1
                framevars[f['t']['alivePlayers']+8] = 1
            if ctmaxval < f['ct']['teamEqVal']: #NOT a good way of doing it.
                ctmaxval = f['ct']['teamEqVal']
                framevars.append(float(ctmaxval))
            else:
                framevars.append(float(ctmaxval))
            if tmaxval < f['t']['teamEqVal']: #NOT a good way of doing it.
                tmaxval = f['t']['teamEqVal']
                framevars.append(float(tmaxval))
            else:
                framevars.append(float(tmaxval))
            cthp = 0
            thp = 0
            if f['ct']["players"]:
                for ctplayer in f['ct']["players"]:
                    cthp += ctplayer["hp"]
            if f['t']["players"]:
                for tplayer in f['t']["players"]:
                    thp += tplayer["hp"]
            framevars.append(cthp)
            framevars.append(thp)
            if firstdamage["tick"] > f["tick"] or firstdamage["attackerSide"] == "T":
                framevars.append(0)
            else:
                framevars.append(1)
            if firstdamage["tick"] > f["tick"] or firstdamage["attackerSide"] == "CT":
                framevars.append(0)
            else:
                framevars.append(1)
            if firstdamage["tick"] < f["tick"]:
                if np.abs(firstdamage["xAngleOffsetFirstDamage"]) > 9.:
                    framevars.append(1)
                else:
                    framevars.append(0)
            else:
                framevars.append(0)
            time_since_ctdeath = 9999.
            time_since_tdeath = 9999.
            for k in r["kills"]:
                if f["tick"] > k["tick"]:
                    if (f["tick"]-k["tick"])/tickrate < time_since_ctdeath and k["victimSide"] == "CT":
                        time_since_ctdeath = (f["tick"]-k["tick"])/tickrate
                    elif (f["tick"]-k["tick"])/tickrate < time_since_tdeath and k["victimSide"] == "T":
                        time_since_tdeath = (f["tick"]-k["tick"])/tickrate
            if time_since_ctdeath > 9000.:
                framevars.append(0.)
            else:
                framevars.append(1./(1.+np.square(time_since_ctdeath/3.)))
            if time_since_tdeath > 9000.:
                framevars.append(0.)
            else:
                framevars.append(1./(1.+np.square(time_since_tdeath/3.)))
            framevars.append(r["ctScore"])
            framevars.append(r["tScore"])
            if r['winningSide'] == "CT":
                framevars.append(1)
            else:
                framevars.append(0)
            if N > 100:
                if properlen != len(framevars):
                    raise Exception("Wrong datalength")
                else:
                    train_list.append(framevars)
            else:
                if properlen != len(framevars):
                    raise Exception("Wrong datalength")
                else:
                    test_list.append(framevars)

    # else:
    #     N += 1
    #     for r in data["gameRounds"]:
    #         tmaxval = 0.
    #         ctmaxval = 0.
    #         properlen = 7
    #         for f in r["frames"]:
    #             framevars = []
    #             framevars.append(f['t']['alivePlayers'])
    #             if tmaxval < f['t']['teamEqVal']:
    #                 tmaxval = f['t']['teamEqVal']
    #                 framevars.append(float(tmaxval))
    #             else:
    #                 framevars.append(float(tmaxval))
    #             framevars.append(f['ct']['alivePlayers'])
    #             if ctmaxval < f['ct']['teamEqVal']:
    #                 ctmaxval = f['ct']['teamEqVal']
    #                 framevars.append(float(ctmaxval))
    #             else:
    #                 framevars.append(float(ctmaxval))
    #             framevars.append(f['seconds'])
    #             if f['bombPlanted']:
    #                 framevars.append(1.)
    #             else:
    #                 framevars.append(0.)
    #             if r['winningSide'] == "CT":
    #                 framevars.append(1)
    #             else:
    #                 framevars.append(0)
    #             if properlen != len(framevars):
    #                 raise Exception("Wrong datalength")
    #             else:
    #                 test_list.append(framevars)



json.dump(train_list, open("traindata.json", 'w'))
json.dump(test_list, open("testdata.json", 'w'))
