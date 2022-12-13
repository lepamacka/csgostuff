from awpy.parser import DemoParser
from awpy.analytics.hltvstats import pros_dont_fake
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind
import numpy as np

parser = DemoParser()
datalist = []
paths = open("demopaths.txt").read().split()

for path in paths:
#    if path[-6] == "e" and path[-7] == "g":
        datalist.append(parser.read_json(path))

defusestats_list = []
for data in datalist:
    defusestats_list += pros_dont_fake(data["gameRounds"])

fake_wins = 0
totalfakes = 0
dontfake_wins = 0
totaldontfakes = 0
for defattempt in defusestats_list:
    if defattempt["deadCTs"] == 4:
        if defattempt["defuseFakes"] > 0:
            totalfakes += 1
            if defattempt["defuse"]:
                fake_wins += 1
        else:
            totaldontfakes += 1
            if defattempt["defuse"]:
                dontfake_wins += 1

fkpop1 = [0]*(totalfakes-fake_wins) + [1]*fake_wins
fkpop2 = [0]*(totaldontfakes-dontfake_wins) + [1]*dontfake_wins

print("Does faking at least once lead to a win:")

print(ttest_ind(fkpop1, fkpop2, equal_var = False, alternative = "less"))

print(totalfakes)
print(totaldontfakes)
print(fake_wins/totalfakes)
print(dontfake_wins/totaldontfakes)
