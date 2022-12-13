import random
import numpy as np

class Team:
    def __init__(self, name, initialseed, skill=0):
        self.skill = skill
        self.name = name
        self.initialseed = initialseed
        self.prevopps = []
        self.record = [0, 0]
    def __str__(self):
        return self.name
    def scorediff(self):
        return self.record[0]-self.record[1]
    def win(self):
        self.record[0] += 1
    def lose(self):
        self.record[1] += 1

random.seed()

def matchresult(team1, team2, matchtype, skillfactor = 0.8):
    res = random.random()
    team1.prevopps.append(team2)
    team2.prevopps.append(team1)
    threshold = 0.5
    if matchtype == "logistic":
        threshold = 1/(1+np.exp(skillfactor*(team2.skill-team1.skill)))
    elif matchtype == "binary":
        threshold = skillfactor
    else:
        print("You need to select a matchtype in swiss().")
    if team1.skill > team2.skill or matchtype == "logistic":
        if res < threshold:
            team1.win()
            team2.lose()
            #return [team1, team2]
        else:
            team2.win()
            team1.lose()
            #return [team2, team1]
    elif team1.skill < team2.skill:
        if res > threshold:
            team1.win()
            team2.lose()
            #return [team1, team2]
        else:
            team2.win()
            team1.lose()
            #return [team2, team1]
    else:
        if res > 0.5:
            team1.win()
            team2.lose()
            #return [team1, team2]
        else:
            team2.win()
            team1.lose()
            #return [team2, team1]

def matches(teams, matchtype, skillfactor):
    if len(teams)%2 > 0:
        print("Wrong number of teams with the same record, must divide by 2 evenly.")
        return
    elif len(teams) == 0:
        return
    else:
        for ind1 in range(len(teams)//2):
            ind2 = len(teams)-ind1-1
            matchresult(teams[ind1], teams[ind2], matchtype, skillfactor)
        return

def buchholz_sort(teams, initseed = True):
    sortlists = []
    for ind in range(len(teams)):
        points = 0
        for prevopp in teams[ind].prevopps:
            points += prevopp.record[0]-prevopp.record[1]
        sortlists.append([teams[ind], points, teams[ind].initialseed])
    sortlists.sort(key=lambda x: x[2])
    sortlists.sort(key=lambda x: x[1], reverse=True)
    #for x in sortlists:
        #print(x[0])
    #    print(x[1])
    #    print(x[2])
    return [sublist[0] for sublist in sortlists]

def buchholz_sort(teams, sorttype = "basicsort"):
    sortlists = []
    for ind in range(len(teams)):
        points = 0
        for prevopp in teams[ind].prevopps:
            points += prevopp.record[0]-prevopp.record[1]
        sortlists.append([teams[ind], points, teams[ind].initialseed])
    sortlists.sort(key=lambda x: x[2])
    sortlists.sort(key=lambda x: x[1], reverse=True)
    #for x in sortlists:
        #print(x[0])
    #    print(x[1])
    #    print(x[2])
    return [sublist[0] for sublist in sortlists]

def swiss(teams, sorttype="buchholz", matchtype="binary", skillfactor=0.5):
    if len(teams)%16 > 0:
        print("Wrong number of teams, must divide by 16 evenly.")
        return
    exitnum = (len(teams)/16)*3
    round = 0
    while round < 4+len(teams)/16:
        testrecord = [0, 0]
        templist = []
        for ind in range(len(teams)):
            if teams[ind].record[0] == exitnum or teams[ind].record[1] == exitnum:
                matches(buchholz_sort([teams[i] for i in templist], sorttype), matchtype, skillfactor)
                templist = []
            elif testrecord == teams[ind].record:
                templist.append(ind)
                if ind == len(teams)-1:
                    matches(buchholz_sort([teams[i] for i in templist], sorttype), matchtype, skillfactor)
            else:
                testrecord = teams[ind].record
                matches(buchholz_sort([teams[i] for i in templist], sorttype), matchtype, skillfactor)
                templist = [ind]
        teams.sort(key=lambda x: x.record[0], reverse=True)
        teams.sort(key=lambda x: x.record[1])
        round += 1

    #for team in teams:
    #    print(team.name + ": " + str(team.record))



if __name__ == "__main__":
    seed = range(16)
    skill = range(16)
    skill.reverse()

    teamlist = []
    A = Team("A", 0, 0)
    i = 0

    while A.record[1] != 3:
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
        teamlist = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]
        swiss(teamlist)
        i+=1

    for team in teamlist:
        print(team.name + ": " + str(team.record))
    print(i)

    #matches(teamlist)
    #for team in teamlist:
    #    print(team.name + ": " + str(team.record))

    # A.prevopps = [H, G]
    # A.record = [2, 0]
    # B.prevopps = [G, H]
    # B.record = [1, 1]
    # C.prevopps = [F, D]
    # C.record = [1, 1]
    # D.prevopps = [E, C]
    # D.record = [2, 0]
    # E.prevopps = [D, F]
    # E.record = [1, 1]
    # F.prevopps = [C, E]
    # F.record = [0, 2]
    # G.prevopps = [B, A]
    # G.record = [1, 1]
    # H.prevopps = [A, B]
    # H.record = [0, 2]
    #
    # list = buchholz_sort([A, B, C, D, E, F, G, H])

    #for team in list:
    #    print(team)
