from awpy.parser import DemoParser
from awpy.analytics.hltvstats import player_stats
from awpy.analytics.hltvstats import firstdmgangle_stats
from awpy.analytics.hltvstats import firstkillangle_stats
from awpy.analytics.hltvstats import dmgangle_stats
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind
import numpy as np
import os, glob, json

def totalstats(stats):
    totdict = {}
    totarray = np.array([[0.]*37]*10)
    playercount = 0
    playerlist = []
    for p1 in stats.keys():
        if p1[-2] == "C":
            pass
        else:
            for p2 in stats.keys():
                if (p1 != p2 and p1[0:16] == p2[0:16]):
                    playerlist.append(stats[p1]["playerName"])
                    totdict[str(stats[p1]["steamID"]) + " - " + stats[p1]["playerName"]] = {
                    "steamID": stats[p1]["steamID"],
                    "playerName": stats[p1]["playerName"],
                    "teamName": stats[p1]["teamName"],
                    "ct_totalRounds": stats[p2]["totalRounds"],
                    "t_totalRounds": stats[p1]["totalRounds"],
                    "ct_kills": stats[p2]["kills"],
                    "t_kills": stats[p1]["kills"],
                    "ct_deaths": stats[p2]["deaths"],
                    "t_deaths": stats[p1]["deaths"],
                    "ct_assistedKills": stats[p2]["assistedKills"],
                    "t_assistedKills": stats[p1]["assistedKills"],
                    "ct_tradeDeaths": stats[p2]["tradeDeaths"],
                    "t_tradeDeaths": stats[p1]["tradeDeaths"],
                    "ct_totalDamageGiven": stats[p2]["totalDamageGiven"],
                    "t_totalDamageGiven": stats[p1]["totalDamageGiven"],
                    "ct_kast": stats[p2]["kast"],
                    "t_kast": stats[p1]["kast"],
                    "ct_firstKills": stats[p2]["firstKills"],
                    "t_firstKills": stats[p1]["firstKills"],
                    "ct_firstDeaths": stats[p2]["firstDeaths"],
                    "t_firstDeaths": stats[p1]["firstDeaths"],
                    "ct_2k": stats[p2]["2k"],
                    "t_2k": stats[p1]["2k"],
                    "ct_3k": stats[p2]["3k"],
                    "t_3k": stats[p1]["3k"],
                    "ct_4k": stats[p2]["4k"],
                    "t_4k": stats[p1]["4k"],
                    "ct_5k": stats[p2]["5k"],
                    "t_5k": stats[p1]["5k"],
                    "ct_1v1": stats[p2]["1v1"],
                    "t_1v1": stats[p1]["1v1"],
                    "ct_1v2": stats[p2]["1v2"],
                    "t_1v2": stats[p1]["1v2"],
                    "ct_1v3": stats[p2]["1v3"],
                    "t_1v3": stats[p1]["1v3"],
                    "ct_1v4": stats[p2]["1v4"],
                    "t_1v4": stats[p1]["1v4"],
                    "ct_1v5": stats[p2]["1v5"],
                    "t_1v5": stats[p1]["1v5"],
                    "ct_assists": stats[p2]["assists"],
                    "t_assists": stats[p1]["assists"]
                    }
                    totarray[playercount][0] = stats[p2]["kills"]/stats[p2]["totalRounds"]
                    totarray[playercount][1] = stats[p1]["kills"]/stats[p1]["totalRounds"]
                    totarray[playercount][2] = (stats[p2]["totalRounds"]-stats[p2]["deaths"])/stats[p2]["totalRounds"]
                    totarray[playercount][3] = (stats[p1]["totalRounds"]-stats[p1]["deaths"])/stats[p1]["totalRounds"]
                    totarray[playercount][4] = (stats[p2]["assistedKills"])/stats[p2]["totalRounds"]
                    totarray[playercount][5] = (stats[p1]["assistedKills"])/stats[p1]["totalRounds"]
                    totarray[playercount][6] = stats[p2]["tradeDeaths"]/stats[p2]["totalRounds"]
                    totarray[playercount][7] = stats[p1]["tradeDeaths"]/stats[p1]["totalRounds"]
                    totarray[playercount][8] = stats[p2]["totalDamageGiven"]/stats[p2]["totalRounds"]
                    totarray[playercount][9] = stats[p1]["totalDamageGiven"]/stats[p1]["totalRounds"]
                    totarray[playercount][10] = stats[p2]["kast"]/stats[p2]["totalRounds"]
                    totarray[playercount][11] = stats[p1]["kast"]/stats[p1]["totalRounds"]
                    totarray[playercount][12] = stats[p2]["firstKills"]/stats[p2]["totalRounds"]
                    totarray[playercount][13] = stats[p1]["firstKills"]/stats[p1]["totalRounds"]
                    totarray[playercount][14] = (stats[p2]["totalRounds"]-stats[p2]["firstDeaths"])/stats[p2]["totalRounds"]
                    totarray[playercount][15] = (stats[p1]["totalRounds"]-stats[p1]["firstDeaths"])/stats[p1]["totalRounds"]
                    totarray[playercount][16] = stats[p2]["2k"]/stats[p2]["totalRounds"]
                    totarray[playercount][17] = stats[p1]["2k"]/stats[p1]["totalRounds"]
                    totarray[playercount][18] = stats[p2]["3k"]/stats[p2]["totalRounds"]
                    totarray[playercount][19] = stats[p1]["3k"]/stats[p1]["totalRounds"]
                    totarray[playercount][20] = stats[p2]["4k"]/stats[p2]["totalRounds"]
                    totarray[playercount][21] = stats[p1]["4k"]/stats[p1]["totalRounds"]
                    totarray[playercount][22] = stats[p2]["5k"]/stats[p2]["totalRounds"]
                    totarray[playercount][23] = stats[p1]["5k"]/stats[p1]["totalRounds"]
                    totarray[playercount][24] = stats[p2]["1v1"]/stats[p2]["totalRounds"]
                    totarray[playercount][25] = stats[p1]["1v1"]/stats[p1]["totalRounds"]
                    totarray[playercount][26] = stats[p2]["1v2"]/stats[p2]["totalRounds"]
                    totarray[playercount][27] = stats[p1]["1v2"]/stats[p1]["totalRounds"]
                    totarray[playercount][28] = stats[p2]["1v3"]/stats[p2]["totalRounds"]
                    totarray[playercount][29] = stats[p1]["1v3"]/stats[p1]["totalRounds"]
                    totarray[playercount][30] = stats[p2]["1v4"]/stats[p2]["totalRounds"]
                    totarray[playercount][31] = stats[p1]["1v4"]/stats[p1]["totalRounds"]
                    totarray[playercount][32] = stats[p2]["1v5"]/stats[p2]["totalRounds"]
                    totarray[playercount][33] = stats[p1]["1v5"]/stats[p1]["totalRounds"]
                    totarray[playercount][34] = (stats[p2]["assists"]+stats[p2]["flashAssists"])/stats[p2]["totalRounds"]
                    totarray[playercount][35] = (stats[p1]["assists"]+stats[p1]["flashAssists"])/stats[p1]["totalRounds"]
                    totarray[playercount][36] = 1
                    playercount += 1
    return totarray#, playerlist, totdict

def psort(origplayers, players): #Returns a list of indices to be used for sorting origplayers.
    if len(origplayers) != len(players):
        print("Not equal players in origplayers and players for playersort.")
        print(origplayers)
        print(players)
        return
    res = [0]*len(players)
    for ind in range(len(players)):
        i=0
        while players[ind] != origplayers[i] and players[ind] != origplayers[i]+" ":
            i+=1
            if i >= 10:
                print("Player name not matched.")
                print(origplayers)
                print(players)
                return
        res[ind] = i
    return res


# parser = DemoParser()
# datalist = []
# paths = open("demopaths.txt").read().split()
#
# for path in paths:
# #    if path[-6] == "e" and path[-7] == "g":
#         datalist.append(parser.read_json(path))

# dontgotoolong = 0
allrounds = 0
ctwins = 0
fdanglestats_list = []
dmgkillanglestats_list = []
fkanglestats_list = []
parser = DemoParser()
estapath = './esta-main/data/lan'
for filename in glob.glob(os.path.join(estapath, '*.json')):
    print(filename)
    # dontgotoolong += 1
    # if dontgotoolong >30:
    #     break
    data = parser.read_json(filename)
    for r in data["gameRounds"]:
        if r["tBuyType"] == r["ctBuyType"]:
            allrounds += 1
            if r["winningSide"] == "CT":
                ctwins += 1
    fdanglestats_list += firstdmgangle_stats(data["gameRounds"])
    fkanglestats_list += firstkillangle_stats(data["gameRounds"])
#    dmgkillanglestats_list += dmgangle_stats(data["gameRounds"])

print("\n" + str(allrounds) + " rounds overall with equal buys. CT win percentage: " + str(ctwins/allrounds) + "\n")

# fkanglestats_list = []
# for data in datalist:
#     fkanglestats_list += firstkillangle_stats(data["gameRounds"], "CT")


fk_wins = 0
totalrounds = 0
fk_wins2 = 0
totalrounds2 = 0
for firstkill in fkanglestats_list:
    if firstkill["attackerSide"] == "CT":
        if np.abs(firstkill["xAngleOffsetFirstKill"])<9:
            totalrounds += 1
            if firstkill["winningTeam"] == firstkill["attackerTeam"]:
                fk_wins += 1
        else:
            totalrounds2 += 1
            if firstkill["winningTeam"] == firstkill["attackerTeam"]:
                fk_wins2 += 1
fkpop1 = [0]*(totalrounds-fk_wins) + [1]*fk_wins
fkpop2 = [0]*(totalrounds2-fk_wins2) + [1]*fk_wins2

print("Damage leading to first kills resulting in wins, either surprised or not: \n")

# print(ttest_ind(fkpop1, fkpop2, equal_var = False, alternative = "less"))

print("Not surprised first kill led to winrate of " + str(fk_wins/totalrounds) + " across " + str(totalrounds) + " rounds.")
print("Surprised first kill led to winrate of " + str(fk_wins2/totalrounds2) + " across " + str(totalrounds2) + " rounds. \n")

#
# dmgkillanglestats_list = []
# for data in datalist:
#     dmgkillanglestats_list += dmgangle_stats(data["gameRounds"])
# #
# totalattempts = 0
# dmgkills_surprised = 0
# dmgkills_notsurprised = 0
# totalattempts_surprised = 0
# totalattempts_notsurprised = 0
# for dmgkillangstat in dmgkillanglestats_list:
# #    if dmgkillangstat["weaponClass"] == "Rifle":
#         if dmgkillangstat["attackerSide"] and not dmgkillangstat["xAngleOffsetAlert"]:
#             totalattempts += 1
#             if np.abs(dmgkillangstat["xAngleOffsetNotalert"])>9:
#                 totalattempts_surprised += 1
#                 if dmgkillangstat["ledToKill"]:
#                     dmgkills_surprised += 1
#             else:
#                 totalattempts_notsurprised += 1
#                 if dmgkillangstat["ledToKill"]:
#                     dmgkills_notsurprised += 1
# dmgkillpop1 = [0]*(totalattempts_surprised-dmgkills_surprised) + [1]*dmgkills_surprised
# dmgkillpop2 = [0]*(totalattempts_notsurprised-dmgkills_notsurprised) + [1]*dmgkills_notsurprised
#
# print("Damage possibly leading to kills:")
#
# print(ttest_ind(dmgkillpop1, dmgkillpop2, equal_var = False, alternative = "less"))
#
# print(totalattempts_surprised)
# print(totalattempts_notsurprised)
# print(dmgkills_surprised/totalattempts_surprised)
# print(dmgkills_notsurprised/totalattempts_notsurprised)


# fdanglestats_list = []
# for data in datalist:
#     fdanglestats_list += firstdmgangle_stats(data["gameRounds"], "CT")


fd_wins_notsurprised = 0
fd_kills_notsurprised = 0
fd_rounds_notsurprised = 0
fd_wins_surprised = 0
fd_kills_surprised = 0
fd_rounds_surprised = 0
# surpr_armor = 0
# non_surpr_armor = 0
for firstdmg in fdanglestats_list:
    if firstdmg["winningSide"] == "CT": #and firstdmg["weaponClass"] == "Rifle"
        if np.abs(firstdmg["xAngleOffsetFirstDamage"])<9:
            fd_rounds_notsurprised += 1
            if firstdmg["winningTeam"] == firstdmg["attackerTeam"]:
                fd_wins_notsurprised += 1
            if firstdmg["ledToKill"]:
                fd_kills_notsurprised += 1
                # if firstdmg["armorDamage"] != 0:
                #     non_surpr_armor += 1
        else:
            fd_rounds_surprised += 1
            if firstdmg["winningTeam"] == firstdmg["attackerTeam"]:
                fd_wins_surprised += 1
            if firstdmg["ledToKill"]:
                fd_kills_surprised += 1
                # if firstdmg["armorDamage"] != 0:
                #     surpr_armor += 1
fdpop1 = [0]*(fd_rounds_notsurprised-fd_wins_notsurprised) + [1]*fd_wins_notsurprised
fdpop2 = [0]*(fd_rounds_surprised-fd_wins_surprised) + [1]*fd_rounds_surprised

# print(non_surpr_armor)
# print(surpr_armor)
print("First Damage leading to kill, either surprised or not: \n")

print("Not surprised first damage led to killrate of " + str(fd_kills_notsurprised/fd_rounds_notsurprised) + " across " + str(fd_rounds_notsurprised) + " rounds.")
print("Surprised first damage led to killrate of " + str(fd_kills_surprised/fd_rounds_surprised) + " across " + str(fd_rounds_surprised) + " rounds. \n")


print("First Damage leading to win, either surprised or not: \n")

# print(ttest_ind(fdpop1, fdpop2, equal_var = False, alternative = "less"))
# print((fd_wins_notsurprised+fd_wins_surprised)/(fd_rounds_surprised+fd_rounds_notsurprised))

print("Not surprised first damage led to winrate of " + str(fd_wins_notsurprised/fd_rounds_notsurprised) + " across " + str(fd_rounds_notsurprised) + " rounds.")
print("Surprised first damage led to winrate of " + str(fd_wins_surprised/fd_rounds_surprised) + " across " + str(fd_rounds_surprised) + " rounds. \n")

json.dump(fdanglestats_list, open("firstdeathangles.json", 'w'))

# totalarray = 0
# for playerstats in playerstats_list:

# totdict1, totarray1, plist1 = totalstats(stats1)
# totdict2, totarray2, plist2 = totalstats(stats2)
# totdict3, totarray3, plist3 = totalstats(stats3)
# totdict4, totarray4, plist4 = totalstats(stats4)
# totdict5, totarray5, plist5 = totalstats(stats5)
# totdict6, totarray6, plist6 = totalstats(stats6)
#
# plist_1to5 = plist1+plist2+plist3+plist4+plist5
#
# totalarray_1to5 = np.append(totarray1,np.append(totarray2,np.append(totarray3,np.append(totarray4,totarray5,axis=0),axis=0),axis=0),axis=0)
# totalarray_1to4 = np.append(totarray1,np.append(totarray2,np.append(totarray3,totarray4,axis=0),axis=0),axis=0)
# # print(totarray1.shape)
# # print(totalarray.shape)
#
# origmaps_1to5 = ["fazeheroicoverpass", "fazeheroicinferno", "fazeheroicmirage", "fazenipoverpass", "fazenipnuke"]
# origplayerlist_1to5 = ['jabbi', 'sjuush', 'cadiaN', 'TeSeS', 'stavn', 'ropz', 'Twistzz', 'broky ', 'rain ', 'karrigan', 'rain ', 'Twistzz', 'broky ', 'ropz', 'karrigan', 'jabbi', 'stavn', 'cadiaN', 'sjuush', 'TeSeS', 'broky ', 'karrigan', 'rain ', 'ropz', 'Twistzz', 'sjuush', 'stavn', 'cadiaN', 'jabbi', 'TeSeS', 'Brollan', 'hampus', 'es3tag', 'Aleksib', 'REZ', 'ropz', 'rain ', 'karrigan', 'broky ', 'Twistzz', 'ropz', 'rain ', 'karrigan', 'broky ', 'Twistzz', 'Brollan', 'hampus', 'es3tag', 'Aleksib', 'REZ']
# origratings_1to5 = np.array([1.16, 0.94, 1.39, 1.20, 0.92, 1.36, 0.72, 1.13, 0.86, 0.85,
#                 1.06, 1.09, 1.26, 1.50, 0.66, 1.13, 0.92, 0.88, 1.05, 1.10,
#                 1.16, 0.67, 0.74, 1.23, 1.17, 1.28, 1.32, 0.81, 1.31, 0.81,
#                 0.85, 0.57, 1.13, 1.53, 1.16, 0.80, 1.41, 0.63, 1.42, 0.86,
#                 1.42, 0.80, 0.87, 1.06, 1.00, 1.09, 1.08, 1.06, 0.80, 1.07])
#
# oplist1 = origplayerlist_1to5[0:10]
# oplist2 = origplayerlist_1to5[10:20]
# oplist3 = origplayerlist_1to5[20:30]
# oplist4 = origplayerlist_1to5[30:40]
# oplist5 = origplayerlist_1to5[40:50]
#
# ratings1 = origratings_1to5[0:10]
# ratings2 = origratings_1to5[10:20]
# ratings3 = origratings_1to5[20:30]
# ratings4 = origratings_1to5[30:40]
# ratings5 = origratings_1to5[40:50]
#
# ratings_1to5 = np.append(ratings1[psort(oplist1,plist1)],np.append(ratings2[psort(oplist2,plist2)],np.append(ratings3[psort(oplist3,plist3)],np.append(ratings4[psort(oplist4,plist4)],ratings5[psort(oplist5,plist5)]))))
# ratings_1to4 = np.append(ratings1[psort(oplist1,plist1)],np.append(ratings2[psort(oplist2,plist2)],np.append(ratings3[psort(oplist3,plist3)],(ratings4[psort(oplist4,plist4)]))))
# # print(ratings_1to5.shape)
# #
# # print(plist_1to5)
#
#
# factors = np.linalg.lstsq(totalarray_1to4, ratings_1to4, rcond = None)
# print(factors[0].shape)
# print(stats6["76561198201620490 - broky _CT"])
# for i in range(50):
#     print(plist_1to5[i] + ": " + str(np.dot(totalarray[i], factors[0])) + " real:" + str(ratings_1to5[i]) + " diff:" + str(ratings_1to5[i]-np.dot(totalarray[i], factors[0])))

# for i in range(10):
    # print(plist6[i] + ": " + str(np.dot(totalarray[i], factors[0])))

#print(totarray5)
#print(factors[0])
#print(factors)
# print(totalarray)
# print(totarray1)
# print(max(ratings_1to5-np.dot(totalarray, factors[0])))
