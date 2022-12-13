import random
import numpy as np
from funcs import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # seed = list(range(16))
    # skill = [11]*8 + [1]*8
    skill = list(range(16, 0, -1))
    res = [0]*9
    qualnums = [0]*16
    i = 0
    totnum = 10000
    seedsum = [0]*16
    while i < totnum:
        # random.shuffle(seed)
        seed = [-1]*16
        k = 0
        while k < 16:
            j = 0
            done = False
            while j < 16 and not done:
                if random.random() > 0.5 and seed[j] == -1:
                    seed[j] = k
                    done = True
                elif j == 15:
                    j = 0
                else:
                    j += 1
            k += 1
        # for ind in range(len(seedsum)):
        #     seedsum[ind] += seed[ind]
        A = Team("A", seed[0], skill[0])
        B = Team("B", seed[1], skill[1])
        C = Team("C", seed[2], skill[2])
        D = Team("D", seed[3], skill[3])
        E = Team("E", seed[4], skill[4])
        F = Team("F", seed[5], skill[5])
        G = Team("G", seed[6], skill[6])
        H = Team("H", seed[7], skill[7])
        I = Team("I", seed[8], skill[8])
        J = Team("J", seed[9], skill[9])
        K = Team("K", seed[10], skill[10])
        L = Team("L", seed[11], skill[11])
        M = Team("M", seed[12], skill[12])
        N = Team("N", seed[13], skill[13])
        O = Team("O", seed[14], skill[14])
        P = Team("P", seed[15], skill[15])
        origteamlist = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]
        teamlist = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]
        swiss(teamlist, "buchholz", "logistic", 0.2)
        # corrqual = 0
        # for team in teamlist:
        #     if team.skill > 8 and team.record[0] == 3:
        #         corrqual += 1
        # res[corrqual] += 1
        for ind in range(len(teamlist)):
            if origteamlist[ind].record[0] == 3:
                qualnums[ind] = qualnums[ind] + (1/totnum)
        i += 1
    print(qualnums)
    print(seedsum)
    plt.bar(range(1, 17), qualnums, tick_label = [origteamlist[j] for j in range(16)])
    plt.yticks(np.linspace(0,1,11), [str(x)+"0%" for x in [""]+list(range(1,11))])
    plt.grid(True, axis = "y")
    plt.axis([-0.2, 17.2, 0, 1])
    plt.show()

    # for team in teamlist:
    #     print(team.name + ": " + str(team.record))
    # print(i)
