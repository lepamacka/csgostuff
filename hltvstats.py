import pandas as pd
import numpy as np

# accuracy
# kast
# adr
# kill stats
# flash stats
# econ stats

def pros_dont_fake(game_rounds):
    defuse_statistics = []
    for r in game_rounds:
        last_tdeath_tick = 0
        dead_t = 0
        dead_ct = 0
        for i, k in enumerate(r["kills"]):
            if k["victimSide"] == "T" and last_tdeath_tick < k["tick"]:
                last_tdeath_tick = k["tick"]
                dead_t += 1
            if k["victimSide"] == "CT" and r["endTick"] > k["tick"]:
                dead_ct += 1
        defuse_attempt = False
        defuse = False
        defuse_contested = False
        defuse_fakes = 0
        defuse_deaths = 0
        defuse_stops = 0
        defuse_startingticks = []
        for b in r["bombEvents"]:
            if b["bombAction"] == "defuse_start" and (last_tdeath_tick > b["tick"] or dead_t < 5):
                defuse_attempt = True
                defuse_startingticks.append(b["tick"])
            if b["bombAction"] == "defuse":
                defuse = True
            if b["bombAction"] == "defuse" and (last_tdeath_tick > b["tick"] or dead_t < 5):
                defuse_contested = True
            if b["bombAction"] == "defuse_aborted" and (last_tdeath_tick > b["tick"] or dead_t < 5):
                defuse_death = False
                for i, k in enumerate(r["kills"]):
                    if k["tick"] == b["tick"] and k["victimName"] == b["playerName"]:
                        defuse_death = True
                        defuse_deaths += 1
                if not defuse_death:
                    defuse_stops += 1
                    defuse_fake = False
                    for defuse_starttick in defuse_startingticks:
                        if b["tick"] < defuse_starttick + 32:
                            defuse_fake = True
                    if defuse_fake:
                        defuse_fakes += 1
        if defuse_attempt:
            defusedict = {"roundData": r.copy(),
            "defuse": defuse,
            "defuseContested": defuse_contested,
            "defuseDeaths": defuse_deaths,
            "defuseStops": defuse_stops,
            "defuseFakes": defuse_fakes,
            "deadCTs": dead_ct,
            }
            defuse_statistics.append(defusedict)
    return defuse_statistics



def firstdmgangle_stats(game_rounds, side = None, equalbuys = True): #Xviewangle etc of first player being shot in a round, can condition on side t or ct.
    firstdmgangle_statistics = []
    # killangle_statistics = []
    for r in game_rounds:
        firstdamage = {"tick": 9999999999}
        for d in r["damages"]:
            if (d["attackerSide"] == side or side == None) and (d["attackerSide"] != d["victimSide"] and d["attackerSide"]): #d["attackerSteamID"] == firstkill["attackerSteamID"]
                if d["tick"] < firstdamage["tick"] and d["weaponClass"] != "Grenade":
                    firstdamage = d.copy()
        if firstdamage["tick"] < 9999999999:
            #xangoff = (firstdamage["attackerViewX"] + 540. - firstdamage["victimViewX"])%360.
            xangoff = (180./np.pi * np.arccos((firstdamage["victimX"] - firstdamage["attackerX"])/np.linalg.norm([firstdamage["victimX"] - firstdamage["attackerX"], firstdamage["victimY"] - firstdamage["attackerY"]])) * np.sign(firstdamage["victimY"] - firstdamage["attackerY"]) + 540. - firstdamage["victimViewX"])%360.
            if xangoff > 180.:
                xangoff = xangoff - 360.
            firstdamage["xAngleOffsetFirstDamage"] = xangoff
            firstdamage["roundNum"] = r["roundNum"]
            firstdamage["winningSide"] = r["winningSide"]
            firstdamage["winningTeam"] = r["winningTeam"]
            firstdamage["ledToKill"] = False
            for i, k in enumerate(r["kills"]):
                if k["victimSteamID"] == firstdamage["victimSteamID"] and k["tick"] < firstdamage["tick"]+640: #and k["attackerSteamID"] == newdmg["attackerSteamID"]
                    firstdamage["ledToKill"] = True
            if r["tBuyType"] == r["ctBuyType"] or not equalbuys:
                firstdmgangle_statistics.append(firstdamage)
    return firstdmgangle_statistics

def firstkillangle_stats(game_rounds, side = None, equalbuys = True): #Xviewangle etc at moment of first damage by eventual killer, for the first kill of the round.
    firstkillangle_statistics = []
    # killangle_statistics = []
    for r in game_rounds:
        firstkill = {"tick": 9999999999}
        for i, k in enumerate(r["kills"]):
            if k["attackerSteamID"] and (k["attackerSide"] == side or side == None):
                if k["tick"] < firstkill["tick"]:
                    firstkill = k.copy()
        if firstkill["tick"] < 9999999999:
            firstdamage = {"tick": 9999999999}
            for d in r["damages"]:
                if d["victimSteamID"] == firstkill["victimSteamID"] and (d["attackerSide"] != d["victimSide"] and d["attackerSteamID"] == firstkill["attackerSteamID"]): #d["attackerSteamID"] == firstkill["attackerSteamID"]
                    if d["tick"] < firstdamage["tick"] and d["weaponClass"] != "Grenade":
                        firstdamage = d.copy()
            if firstdamage["tick"] < 9999999999:
                #xangoff = (firstdamage["attackerViewX"] + 540. - firstdamage["victimViewX"])%360.
                xangoff = (180./np.pi * np.arccos((firstdamage["victimX"] - firstdamage["attackerX"])/np.linalg.norm([firstdamage["victimX"] - firstdamage["attackerX"], firstdamage["victimY"] - firstdamage["attackerY"]])) * np.sign(firstdamage["victimY"] - firstdamage["attackerY"]) + 540. - firstdamage["victimViewX"])%360.
                if xangoff > 180.:
                    xangoff = xangoff - 360.
                firstdamage["xAngleOffsetFirstKill"] = xangoff
                firstdamage["roundNum"] = r["roundNum"]
                firstdamage["winningSide"] = r["winningSide"]
                firstdamage["winningTeam"] = r["winningTeam"]
                if r["tBuyType"] == r["ctBuyType"] or not equalbuys:
                    firstkillangle_statistics.append(firstdamage)
    return firstkillangle_statistics

def dmgangle_stats(game_rounds, equalbuys = True): #Xviewangle etc at the moment of damage relative to attacker position.
    dmgangle_statistics = []     #With or without having attacked or been attacked by attacker recently.
    # killangle_statistics = []
    for r in game_rounds:
        rnddmgstats = []
        for d in r["damages"]:
            newdmg = {}
            newdmg = d.copy()
            alert = False
            for prev in rnddmgstats:
                if d["victimName"] == prev["victimName"] and d["attackerName"] == prev["attackerName"]:
                    if d["tick"]-prev["tick"] < 1792:
                        alert = True
                elif d["attackerName"] == prev["victimName"] and d["victimName"] == prev["attackerName"]:
                    if d["tick"]-prev["tick"] < 1792:
                        alert = True
            if not d["attackerSteamID"]:
                pass
            elif d["weaponClass"] == "Grenade":
                pass
            elif alert:
                #xangoff = (newdmg["attackerViewX"] + 540. - newdmg["victimViewX"])%360.
                xangoff = (180./np.pi * np.arccos((newdmg["victimX"] - newdmg["attackerX"])/np.linalg.norm([newdmg["victimX"] - newdmg["attackerX"], newdmg["victimY"] - newdmg["attackerY"]])) * np.sign(newdmg["victimY"] - newdmg["attackerY"]) + 540. - newdmg["victimViewX"])%360.
                if xangoff > 180.:
                    xangoff = xangoff - 360.
                newdmg["xAngleOffsetNotalert"] = False
                newdmg["xAngleOffsetAlert"] = xangoff
                newdmg["ledToKill"] = False
                for i, k in enumerate(r["kills"]):
                    if k["victimSteamID"] == newdmg["victimSteamID"] and k["tick"] < newdmg["tick"]+512: #and k["attackerSteamID"] == newdmg["attackerSteamID"]
                        newdmg["ledToKill"] = True
                if r["tBuyType"] == r["ctBuyType"] or not equalbuys:
                    rnddmgstats.append(newdmg)
                    dmgangle_statistics.append(newdmg)
            else:
                #xangoff = (newdmg["attackerViewX"] + 540. - newdmg["victimViewX"])%360.
                xangoff = (180./np.pi * np.arccos((newdmg["victimX"] - newdmg["attackerX"])/np.linalg.norm([newdmg["victimX"] - newdmg["attackerX"], newdmg["victimY"] - newdmg["attackerY"]])) * np.sign(newdmg["victimY"] - newdmg["attackerY"]) + 540. - newdmg["victimViewX"])%360.
                if xangoff > 180.:
                    xangoff = xangoff - 360.
                newdmg["xAngleOffsetAlert"] = False
                newdmg["xAngleOffsetNotalert"] = xangoff
                newdmg["ledToKill"] = False
                for i, k in enumerate(r["kills"]):
                    if k["victimSteamID"] == newdmg["victimSteamID"] and k["tick"] < newdmg["tick"] + 512: #and k["attackerSteamID"] == newdmg["attackerSteamID"]
                        newdmg["ledToKill"] = True
                if r["tBuyType"] == r["ctBuyType"] or not equalbuys:
                    rnddmgstats.append(newdmg)
                    dmgangle_statistics.append(newdmg)
    return dmgangle_statistics

def killangle_stats(game_rounds, equalbuys = True): #Xviewangle etc at the moment of death relative to killer position.
    killangle_statistics = []
    for r in game_rounds:
        for i, k in enumerate(r["kills"]):
            if k["attackerSteamID"] and k["weaponClass"] != "Grenade":
                kill = k.copy()
                #xangoff = (k["attackerViewX"] + 540. - k["victimViewX"])%360.
                xangoff = (180./np.pi * np.arccos((kill["victimX"] - kill["attackerX"])/np.linalg.norm([kill["victimX"] - kill["attackerX"], kill["victimY"] - kill["attackerY"]])) * np.sign(kill["victimY"] - kill["attackerY"]) + 540. - kill["victimViewX"])%360.
                if xangoff > 180.:
                    xangoff = xangoff - 360.
                kill["xAngleOffset"] = xangoff
                if r["tBuyType"] == r["ctBuyType"] or not equalbuys:
                    killangle_statistics.append(kill)
    return killangle_statistics


def player_stats(game_rounds, return_type="json"):
    player_statistics = {}
    for r in game_rounds:
        # Add players
        ct_side = r["ctSide"]
        t_side = r["tSide"]
        ct_dead_end = []
        t_dead_end = []
        ct_lastdead = None
        t_lastdead = None
        ct_clutchopponents = 0
        t_clutchopponents = 0
        kills_in_round = {}
        for p in ct_side["players"]:
            kills_in_round[str(p["steamID"]) + " - " + p["playerName"] + "_CT"] = {"killsinround": 0}
            if str(p["steamID"]) + " - " + p["playerName"] + "_CT" not in player_statistics:
                player_statistics[str(p["steamID"]) + " - " + p["playerName"] + "_CT"] = {
                    "steamID": p["steamID"],
                    "playerName": p["playerName"],
                    "teamName": ct_side["teamName"],
                    "isBot": True if p["steamID"] == 0 else False,
                    "totalRounds": 0,
                    "kills": 0,
                    "deaths": 0,
                    "kdr": 0,
                    "assists": 0,
                    "assistedKills": 0,
                    "tradeKills": 0,
                    "tradeDeaths": 0,
                    "teamKills": 0,
                    "suicides": 0,
                    "flashAssists": 0,
                    "totalDamageGiven": 0,
                    "totalDamageTaken": 0,
                    "totalTeamDamageGiven": 0,
                    "adr": 0,
                    "totalShots": 0,
                    "shotsHit": 0,
                    "accuracy": 0,
                    "rating": 0,
                    "kast": 0,
                    "hs": 0,
                    "hsPercent": 0,
                    "firstKills": 0,
                    "firstDeaths": 0,
                    "utilityDamage": 0,
                    "smokesThrown": 0,
                    "flashesThrown": 0,
                    "heThrown": 0,
                    "fireThrown": 0,
                    "enemiesFlashed": 0,
                    "teammatesFlashed": 0,
                    "blindTime": 0,
                    "plants": 0,
                    "defuses": 0,
                    "2k": 0,
                    "3k": 0,
                    "4k": 0,
                    "5k": 0,
                    "1v1": 0,
                    "1v2": 0,
                    "1v3": 0,
                    "1v4": 0,
                    "1v5": 0,
                }
                player_statistics[str(p["steamID"]) + " - " + p["playerName"] + "_CT"][
                    "totalRounds"
                ] += 1
            else:
                player_statistics[str(p["steamID"]) + " - " + p["playerName"] + "_CT"][
                    "totalRounds"
                ] += 1
        for p in t_side["players"]:
            kills_in_round[str(p["steamID"]) + " - " + p["playerName"] + "_T"] = {"killsinround": 0}
            if str(p["steamID"]) + " - " + p["playerName"] + "_T" not in player_statistics:
                player_statistics[str(p["steamID"]) + " - " + p["playerName"] + "_T"] = {
                    "steamID": p["steamID"],
                    "playerName": p["playerName"],
                    "teamName": t_side["teamName"],
                    "totalRounds": 0,
                    "kills": 0,
                    "deaths": 0,
                    "kdr": 0,
                    "assists": 0,
                    "assistedKills": 0,
                    "tradeKills": 0,
                    "tradeDeaths": 0,
                    "teamKills": 0,
                    "suicides": 0,
                    "flashAssists": 0,
                    "totalDamageGiven": 0,
                    "totalDamageTaken": 0,
                    "totalTeamDamageGiven": 0,
                    "adr": 0,
                    "totalShots": 0,
                    "shotsHit": 0,
                    "accuracy": 0,
                    "rating": 0,
                    "kast": 0,
                    "hs": 0,
                    "hsPercent": 0,
                    "firstKills": 0,
                    "firstDeaths": 0,
                    "utilityDamage": 0,
                    "smokesThrown": 0,
                    "flashesThrown": 0,
                    "heThrown": 0,
                    "fireThrown": 0,
                    "enemiesFlashed": 0,
                    "teammatesFlashed": 0,
                    "blindTime": 0,
                    "plants": 0,
                    "defuses": 0,
                    "2k": 0,
                    "3k": 0,
                    "4k": 0,
                    "5k": 0,
                    "1v1": 0,
                    "1v2": 0,
                    "1v3": 0,
                    "1v4": 0,
                    "1v5": 0,
                }
                player_statistics[str(p["steamID"]) + " - " + p["playerName"] + "_T"][
                    "totalRounds"
                ] += 1
            else:
                player_statistics[str(p["steamID"]) + " - " + p["playerName"] + "_T"][
                    "totalRounds"
                ] += 1
        kast = {}
        for p in t_side["players"]:
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_T"] = {}
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_T"]["k"] = False
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_T"]["a"] = False
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_T"]["s"] = True
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_T"]["t"] = False
        for p in ct_side["players"]:
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_CT"] = {}
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_CT"]["k"] = False
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_CT"]["a"] = False
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_CT"]["s"] = True
            kast[str(p["steamID"]) + " - " + p["playerName"] + "_CT"]["t"] = False
        # Calculate kills
        for i, k in enumerate(r["kills"]):
            killer_key = str(k["attackerSteamID"]) + " - " + str(k["attackerName"]) + "_" + str(k["attackerSide"])
            victim_key = str(k["victimSteamID"]) + " - " + str(k["victimName"]) + "_" + str(k["victimSide"])
            traded_key = str(k["playerTradedSteamID"]) + " - " + str(k["playerTradedName"]) + "_" + str(k["attackerSide"])
            assister_key = str(k["assisterSteamID"]) + " - " + str(k["assisterName"]) + "_" + str(k["assisterSide"])
            flashthrower_key = (
                str(k["flashThrowerSteamID"]) + " - " + str(k["flashThrowerName"]) + "_" + str(k["flashThrowerSide"])
            )
            if (
                k["attackerSteamID"]
                and not k["isSuicide"]
                and not k["isTeamkill"]
                and killer_key in player_statistics.keys()
            ):
                player_statistics[killer_key]["kills"] += 1
                kast[killer_key]["k"] = True
                kills_in_round[killer_key]["killsinround"] += 1
            if victim_key in player_statistics.keys():
                player_statistics[victim_key]["deaths"] += 1
                kast[victim_key]["s"] = False
                if k["victimSide"] == "CT" and k["tick"] <= r["endTick"]:
                    ct_dead_end.append(victim_key)
                    ct_lastdead = victim_key
                    if len(ct_dead_end) == 4:
                        ct_clutchopponents = 5 - len(t_dead_end)
                if k["victimSide"] == "T" and k["tick"] <= r["endTick"]:
                    t_dead_end.append(victim_key)
                    t_lastdead = victim_key
                    if len(t_dead_end) == 4:
                        t_clutchopponents = 5 - len(ct_dead_end)
            if (
                k["assisterSteamID"]
                and k["assisterTeam"] != k["victimTeam"]
                and assister_key in player_statistics.keys()
            ):
                player_statistics[assister_key]["assists"] += 1
                kast[assister_key]["a"] = True
            if (
                k["assisterSteamID"]
                and assister_key in player_statistics.keys()
            ):
                player_statistics[killer_key]["assistedKills"] += 1
            if (
                k["flashThrowerSteamID"]
                and k["flashThrowerTeam"] != k["victimTeam"]
                and flashthrower_key in player_statistics.keys()
            ):
                player_statistics[flashthrower_key]["flashAssists"] += 1
                kast[flashthrower_key]["a"] = True
            if (
                k["isTrade"]
                and k["attackerSteamID"]
                and k["attackerSide"] != k["victimSide"]
                and k["playerTradedTeam"] == k["attackerTeam"]
                and killer_key in player_statistics.keys()
                and victim_key in player_statistics.keys()
            ):
                player_statistics[killer_key]["tradeKills"] += 1
                player_statistics[traded_key]["tradeDeaths"] += 1
                kast[traded_key]["t"] = True
            if (
                k["isFirstKill"]
                and k["attackerSteamID"]
                and killer_key in player_statistics.keys()
                and victim_key in player_statistics.keys()
            ):
                player_statistics[killer_key]["firstKills"] += 1
                player_statistics[victim_key]["firstDeaths"] += 1
            if (
                k["isTeamkill"]
                and k["attackerSteamID"]
                and killer_key in player_statistics.keys()
            ):
                player_statistics[killer_key]["teamKills"] += 1
            if (
                k["isHeadshot"]
                and k["attackerSteamID"]
                and killer_key in player_statistics.keys()
            ):
                player_statistics[killer_key]["hs"] += 1
            if k["isSuicide"] and victim_key in player_statistics.keys():
                player_statistics[victim_key]["suicides"] += 1
        for d in r["damages"]:
            attacker_key = str(d["attackerSteamID"]) + " - " + str(d["attackerName"]) + "_" + str(d["attackerSide"])
            victim_key = str(d["victimSteamID"]) + " - " + str(d["victimName"]) + "_" + str(d["victimSide"])

            if (
                d["attackerSteamID"]
                and not d["isFriendlyFire"]
                and attacker_key in player_statistics.keys()
            ):
                player_statistics[attacker_key]["totalDamageGiven"] += d[
                    "hpDamageTaken"
                ]
            if d["victimSteamID"] and victim_key in player_statistics.keys():
                player_statistics[victim_key]["totalDamageTaken"] += d["hpDamageTaken"]
            if d["isFriendlyFire"] and attacker_key in player_statistics.keys():
                player_statistics[attacker_key]["totalTeamDamageGiven"] += d[
                    "hpDamageTaken"
                ]
            if (
                d["weaponClass"] not in ["Unknown", "Grenade", "Equipment"]
                and attacker_key in player_statistics.keys()
            ):
                player_statistics[attacker_key]["shotsHit"] += 1
            if (
                d["weaponClass"] == "Grenade"
                and attacker_key in player_statistics.keys()
            ):
                player_statistics[attacker_key]["utilityDamage"] += d["hpDamageTaken"]
        for w in r["weaponFires"]:
            if (
                str(w["playerSteamID"]) + " - " + w["playerName"]
                in player_statistics.keys()
            ):
                player_statistics[str(w["playerSteamID"]) + " - " + w["playerName"]][
                    "totalShots"
                ] += 1
        for f in r["flashes"]:
            flasher_key = str(f["attackerSteamID"]) + " - " + f["attackerName"] + "_" + str(f["attackerSide"])
            player_key = str(f["playerSteamID"]) + " - " + f["playerName"] + "_" + str(f["playerSide"])
            if f["attackerSteamID"] and flasher_key in player_statistics.keys():
                if f["attackerSide"] == f["playerSide"]:
                    player_statistics[flasher_key]["teammatesFlashed"] += 1
                else:
                    player_statistics[flasher_key]["enemiesFlashed"] += 1
                    player_statistics[flasher_key]["blindTime"] += f["flashDuration"]
        for g in r["grenades"]:
            thrower_key = str(g["throwerSteamID"]) + " - " + g["throwerName"] + "_" + str(g["throwerSide"])
            if g["throwerSteamID"] and thrower_key in player_statistics.keys():
                if g["grenadeType"] == "Smoke Grenade":
                    player_statistics[thrower_key]["smokesThrown"] += 1
                if g["grenadeType"] == "Flashbang":
                    player_statistics[thrower_key]["flashesThrown"] += 1
                if g["grenadeType"] == "HE Grenade":
                    player_statistics[thrower_key]["heThrown"] += 1
                if g["grenadeType"] in ["Incendiary Grenade", "Molotov"]:
                    player_statistics[thrower_key]["fireThrown"] += 1
        for b in r["bombEvents"]:
            player_key = str(b["playerSteamID"]) + " - " + b["playerName"]
            if (b["playerSteamID"] and player_key + "_CT") in player_statistics.keys() or (b["playerSteamID"] and player_key + "_T") in player_statistics.keys():
                if b["bombAction"] == "plant":
                    player_statistics[player_key + "_T"]["plants"] += 1
                if b["bombAction"] == "defuse":
                    player_statistics[player_key + "_CT"]["defuses"] += 1
        for player in kast:
            all_true = False
            for component in kast[player]:
                if kast[player][component]:
                    all_true = True
            if all_true:
                player_statistics[player]["kast"] += 1
        for player in kills_in_round:
            if kills_in_round[player]["killsinround"] == 2:
                player_statistics[player]["2k"] += 1
            if kills_in_round[player]["killsinround"] == 3:
                player_statistics[player]["3k"] += 1
            if kills_in_round[player]["killsinround"] == 4:
                player_statistics[player]["4k"] += 1
            if kills_in_round[player]["killsinround"] == 5:
                player_statistics[player]["5k"] += 1
        if ct_clutchopponents > 0 and r["winningSide"] == "CT":
            ct_clutcher = ct_lastdead
            for p in ct_side["players"]:
                p_id = str(p["steamID"]) + " - " + p["playerName"] + "_CT"
                if p_id not in ct_dead_end:
                    ct_clutcher = p_id
            # print(ct_clutcher + " " + str(r["roundNum"]))
            if ct_clutchopponents == 1:
                player_statistics[ct_clutcher]["1v1"] += 1
            if ct_clutchopponents == 2:
                player_statistics[ct_clutcher]["1v2"] += 1
            if ct_clutchopponents == 3:
                player_statistics[ct_clutcher]["1v3"] += 1
            if ct_clutchopponents == 4:
                player_statistics[ct_clutcher]["1v4"] += 1
            if ct_clutchopponents == 5:
                player_statistics[ct_clutcher]["1v5"] += 1
        if t_clutchopponents > 0 and r["winningSide"] == "T":
            t_clutcher = t_lastdead
            for p in t_side["players"]:
                p_id = str(p["steamID"]) + " - " + p["playerName"] + "_T"
                if p_id not in t_dead_end:
                    t_clutcher = p_id
            # print(t_clutcher + " " + str(r["roundNum"]))
            if t_clutchopponents == 1:
                player_statistics[t_clutcher]["1v1"] += 1
            if t_clutchopponents == 2:
                player_statistics[t_clutcher]["1v2"] += 1
            if t_clutchopponents == 3:
                player_statistics[t_clutcher]["1v3"] += 1
            if t_clutchopponents == 4:
                player_statistics[t_clutcher]["1v4"] += 1
            if t_clutchopponents == 5:
                player_statistics[t_clutcher]["1v5"] += 1

    # for player in kast:
    #     player_statistics[player]["kast"] = round(
    #         100
    #         * player_statistics[player]["kast"]
    #         / player_statistics[player]["totalRounds"],
    #         1,
    #     )
    for player in player_statistics:
        player_statistics[player]["blindTime"] = round(
            player_statistics[player]["blindTime"], 2
        )
    for player in player_statistics:
        player_statistics[player]["kdr"] = round(
            player_statistics[player]["kills"] / player_statistics[player]["deaths"]
            if player_statistics[player]["deaths"] != 0
            else player_statistics[player]["kills"],
            2,
        )
    for player in player_statistics:
        player_statistics[player]["adr"] = round(
            player_statistics[player]["totalDamageGiven"]
            / player_statistics[player]["totalRounds"],
            1,
        )
    for player in player_statistics:
        player_statistics[player]["accuracy"] = round(
            player_statistics[player]["shotsHit"]
            / player_statistics[player]["totalShots"]
            if player_statistics[player]["totalShots"] != 0
            else 0,
            2,
        )
    for player in player_statistics:
        player_statistics[player]["hsPercent"] = round(
            player_statistics[player]["hs"] / player_statistics[player]["kills"]
            if player_statistics[player]["kills"] != 0
            else 0,
            2,
        )
    for player in player_statistics:
        impact = (
            2.13
            * (
                player_statistics[player]["kills"]
                / player_statistics[player]["totalRounds"]
            )
            + 0.42
            * (
                player_statistics[player]["assists"]
                / player_statistics[player]["totalRounds"]
            )
            - 0.41
        )
        player_statistics[player]["rating"] = (
            0.0073 * player_statistics[player]["kast"]
            + 0.3591
            * (
                player_statistics[player]["kills"]
                / player_statistics[player]["totalRounds"]
            )
            - 0.5329
            * (
                player_statistics[player]["deaths"]
                / player_statistics[player]["totalRounds"]
            )
            + 0.2372 * (impact)
            + 0.0032 * (player_statistics[player]["adr"])
            + 0.1587
        )
        player_statistics[player]["rating"] = round(
            player_statistics[player]["rating"], 2
        )
    if return_type == "df":
        return (
            pd.DataFrame()
            .from_dict(player_statistics, orient="index")
            .reset_index(drop=True)
        )
    else:
        return player_statistics
