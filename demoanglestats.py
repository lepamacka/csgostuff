from awpy.parser import DemoParser
from awpy.analytics.hltvstats import firstkillangle_stats
from awpy.analytics.hltvstats import dmgangle_stats
from awpy.analytics.hltvstats import killangle_stats
from matplotlib import pyplot as plt
from scipy.stats import wrapcauchy
import numpy as np
import os, glob

# parser = DemoParser()
# datalist = []
# paths = open("demopaths.txt").read().split()
# for path in paths:
#     datalist.append(parser.read_json(path))
#
# fkanglestats_list = []
# for data in datalist:
#     fkanglestats_list += firstkillangle_stats(data["gameRounds"])
#
# dmganglestats_list = []
# for data in datalist:
#     dmganglestats_list += dmgangle_stats(data["gameRounds"])
#
# killanglestats_list = []
# for data in datalist:
#     killanglestats_list += killangle_stats(data["gameRounds"])

iter = 0
fkanglestats_list = []
dmganglestats_list = []
killanglestats_list = []
parser = DemoParser()
estapath = './esta-main/data/lan'
for filename in glob.glob(os.path.join(estapath, '*.json')):
    iter += 1
    # if iter > 10:
    #     break
    print(str(iter) + ": " + filename)
    data = parser.read_json(filename)
    fkanglestats_list += firstkillangle_stats(data["gameRounds"])
    killanglestats_list += killangle_stats(data["gameRounds"])
    dmganglestats_list += dmgangle_stats(data["gameRounds"])

histdata_firstkill = []
histdata_notalert = []
histdata_alert = []
histdata_kill = []
surprised_list = []
angle_limit = 180.
buckets = 1080
cum = True
ylim = 1.

for fkanglestat in fkanglestats_list:
#    if fkanglestat["weapon"] != "AWP":
    if fkanglestat["attackerSide"] == "CT": #and (fkanglestat["weapon"] != "AWP" and fkanglestat["weaponClass"] == "Rifle"):
        if fkanglestat["xAngleOffsetFirstKill"]<angle_limit and fkanglestat["xAngleOffsetFirstKill"]>-angle_limit:
            histdata_firstkill.append(fkanglestat["xAngleOffsetFirstKill"])
for dmgangstat in dmganglestats_list:
#    if dmgangstat["weapon"] != "AWP":
    if dmgangstat["attackerSide"] == "CT": #and (dmgangstat["weapon"] != "AWP" and dmgangstat["weaponClass"] == "Rifle"):
        if dmgangstat["attackerSide"] and not dmgangstat["xAngleOffsetAlert"]:
            if dmgangstat["xAngleOffsetNotalert"]>30. and dmgangstat["xAngleOffsetNotalert"]<-30.:
                surprised_list.append(dmgangstat["xAngleOffsetNotalert"])
            if dmgangstat["xAngleOffsetNotalert"]<angle_limit and dmgangstat["xAngleOffsetNotalert"]>-angle_limit:
                histdata_notalert.append(dmgangstat["xAngleOffsetNotalert"])
        if dmgangstat["attackerSide"] and not dmgangstat["xAngleOffsetNotalert"]:
            if dmgangstat["xAngleOffsetAlert"]<angle_limit and dmgangstat["xAngleOffsetAlert"]>-angle_limit:
                histdata_alert.append(dmgangstat["xAngleOffsetAlert"])
for killanglestat in killanglestats_list:
#    if killanglestat["weapon"] != "AWP":
    if killanglestat["attackerSide"] == "CT": #and (killanglestat["weapon"] != "AWP" and killanglestat["weaponClass"] == "Rifle"):
        if killanglestat["xAngleOffset"]<angle_limit and killanglestat["xAngleOffset"]>-angle_limit:
            histdata_kill.append(killanglestat["xAngleOffset"])
#print(len(surprised_list)/len(histdata))

print(len(histdata_firstkill))
print(len(histdata_notalert))
print(len(histdata_alert))
print(len(histdata_kill))

# c_notalert = wrapcauchy.fit((np.pi/180.)*(histdata_notalert+180.*np.ones(len(histdata_notalert))))
# c_alert = wrapcauchy.fit((np.pi/180.)*(histdata_alert+180.*np.ones(len(histdata_alert))))
# c_kill = wrapcauchy.fit((np.pi/180.)*(histdata_kill+180.*np.ones(len(histdata_kill))))
# x = np.linspace(-angle_limit, angle_limit, buckets)
# p_notalert = wrapcauchy.cdf((np.pi/180.)*(x+180.*np.ones(len(x))), c_notalert)
# p_alert = wrapcauchy.cdf((np.pi/180.)*(x+180.*np.ones(len(x))), c_alert)
# p_kill = wrapcauchy.cdf((np.pi/180.)*(x+180.*np.ones(len(x))), c_kill)

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'

plt.figure()
plt.subplot(311)
plt.title("Lateral viewangle offset from attacker when damaged/killed, cum. prob. density")
#plt.hist(histdata_notalert,buckets,color=CB91_Blue, density = True, cumulative = cum)
plt.plot(np.sort(histdata_notalert), np.linspace(0, 1, len(histdata_notalert), endpoint=False), color=CB91_Green, linewidth = 2)
#plt.title("N = " + str(len(histdata_notalert)))
plt.axis([-angle_limit, angle_limit, 0., ylim])
plt.legend(["first damage"], loc="upper left")
plt.axvline(np.quantile(histdata_notalert, 0.2), color='k', linestyle='dashed', linewidth=1)
print(np.quantile(histdata_notalert, 0.2))
plt.axvline(np.quantile(histdata_notalert, 0.8), color='k', linestyle='dashed', linewidth=1)
print(np.quantile(histdata_notalert, 0.8))
#plt.plot(x, p_notalert, 'k', linewidth=2)
plt.grid(axis = "y")
plt.xticks(np.linspace(-angle_limit, angle_limit, 7), [""]*7)
# plt.xticks([])
plt.subplot(312)
#plt.hist(histdata_alert,buckets,color=CB91_Purple, density = True, cumulative = cum)
plt.plot(np.sort(histdata_alert), np.linspace(0, 1, len(histdata_alert), endpoint=False), color=CB91_Blue, linewidth = 2)
#plt.title("N = " + str(len(histdata_alert)))
plt.axis([-angle_limit, angle_limit, 0., ylim])
#plt.plot(x, p_alert, 'k', linewidth=2)
plt.legend(["other damage"], loc="upper left")
plt.axvline(np.quantile(histdata_alert, 0.2), color='k', linestyle='dashed', linewidth=1)
print(np.quantile(histdata_alert, 0.2))
plt.axvline(np.quantile(histdata_alert, 0.8), color='k', linestyle='dashed', linewidth=1)
print(np.quantile(histdata_alert, 0.8))
plt.grid(axis = "y")
plt.xticks(np.linspace(-angle_limit, angle_limit, 7), [""]*7)
# plt.xticks([])
plt.subplot(313)
# plt.hist(histdata_kill,buckets,color=CB91_Violet, density = True, cumulative = cum)
plt.plot(np.sort(histdata_kill), np.linspace(0, 1, len(histdata_kill), endpoint=False), color=CB91_Purple, linewidth = 2)
#plt.title("N = " + str(len(histdata_kill)))
plt.axis([-angle_limit, angle_limit, 0., ylim])
#plt.plot(x, p_kill, 'k', linewidth=2)
plt.legend(["kills"], loc="upper left")
plt.axvline(np.quantile(histdata_kill, 0.2), color='k', linestyle='dashed', linewidth=1)
print(np.quantile(histdata_kill, 0.2))
plt.axvline(np.quantile(histdata_kill, 0.8), color='k', linestyle='dashed', linewidth=1)
print(np.quantile(histdata_kill, 0.8))
plt.grid(axis = "y")
plt.xticks(np.linspace(-angle_limit, angle_limit, 7))
# plt.subplot(414)
# plt.hist(histdata_firstkill,buckets,color='g', density = True, cumulative = cum)
# #plt.title("N = " + str(len(histdata_notalert)))
# plt.axis([-angle_limit, angle_limit, 0., ylim])
# #plt.plot(x, p_notalert, 'k', linewidth=2)
# plt.legend(["first kill"], loc="upper left")
# plt.grid(axis = "y")
plt.show()
