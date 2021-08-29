import numpy
import math
import random

#S = [1,0,6] #1 -> korist, 0 -> dravec, 6 -> mrtvo
S = [1,2,3,4]

def pottsGetNumOfTilesWithState(state, value_array):
    N = 0
    for i in range(1, len(value_array)):
        if value_array[i] == state: N += 1
    return N


def chooseRandomlyFromArray(state, N, value_array):
    ran = random.random()
    j = 0
    for i in range(1, len(value_array)):
        if value_array[i] == state:
            if ran <= (j+1)/N and ran > j / N:
                return i
            j += 1
    return -800


class Rules:
    CONTACT_P = 0.8
    METASTABLE_ALPHA = 2
    METASTABLE_BETA = 6
    POTTS_BETA = 2

    prey_reproduction = 9/10 #sireni prey
    predator_death = 9/10
    creation = 1/10000    #na prazdnem poli
    predator_creation = 1/10000 #prey -> predator

    def prey(self, value_array):
        prey_num, predator_num = 0, 0
        neigh_num = len(value_array) - 1

        for i in range(1, neigh_num + 1):
            if value_array[i] == 1: prey_num += 1
            elif value_array[i] == 0: predator_num += 1

        if value_array[0] == 1:
            N = pottsGetNumOfTilesWithState(6, value_array) #pocet neobsazenych policek
            if random.random() < self.predator_creation:
                return [0, *value_array[1:]]    #aby nebylo plne pole prey stabilni stav
            if N == 0:  return value_array
            else:
                for i in range(1, len(value_array)):
                    if value_array[i] == 6 and random.random() < self.prey_reproduction:
                        value_array[i] = 1  #sireni na neobsazena policka
                return value_array

        elif value_array[0] == 0:
            N = pottsGetNumOfTilesWithState(1, value_array)
            if N == 0:
                if random.random() < self.predator_death:
                    return [6, *value_array[1:]]    #smrt predatora
                else:   return value_array
            else:
                index = chooseRandomlyFromArray(1, N, value_array)
                value_array[index] = 0  #presun predatora ke koristi
                return value_array

        elif value_array[0] == 6:
            ran = random.random()
            if ran < self.creation:
                return [1, *value_array[1:]]
            elif ran > (1 - self.creation):
                return [0, *value_array[1:]]

        return value_array



    def voter(self, value_array):
        return [value_array[1], value_array[1]]


    def annihilationWalk(self, value_array):
        return [0, (value_array[0] + value_array[1]) % 2]


    def contact(self, value_array):
        rnd = random.random()
        if rnd < self.CONTACT_P: return [value_array[0] or value_array[1], value_array[1]]
        else:   return [0, value_array[1]]


    def potts(self, value_array):
        probability_law_unnormalised = numpy.array( [math.exp(self.POTTS_BETA * pottsGetNumOfTilesWithState(z, value_array)) for z in S] )
        probability_law = numpy.divide( probability_law_unnormalised, numpy.sum(probability_law_unnormalised))

        low = 0
        high = 0
        rnd = random.random()

        for i in range(0, len(S)):
            high += probability_law[i]
            if (rnd > low) and (rnd < high):    output_state = S[i]
            low += probability_law[i]

        value_array[0] = output_state
        return value_array

    #1 -> X=1;Y=1; 2 -> X=1;Y=-1; 3 -> X=-1;Y=1; 4 -> X=-1;Y=-1
    def metastableIsing(self, value_array):
        X = (1 if value_array[0] < 3 else -1)
        Y = (1 if (value_array[0] % 2) == 1 else -1)
        X_new = X
        Y_new = Y

        N = len(value_array) - 1
        F = 0
        if random.random() < 1/2:
            for i in range(1, N+1):
                F += 1 / N  if (value_array[i] < 3 and X == 1) or (value_array[i] > 2 and X == -1) else 0
            flip_probability = math.exp(- self.METASTABLE_BETA * F)
            flip_probability *= math.exp(- self.METASTABLE_ALPHA) if X == Y else 1

            if random.random() < flip_probability:  X_new = -X


        else:
            for i in range(1, N+1):
                F += 1 / N  if ((value_array[i] % 2) == 0 and Y == -1) or ( (value_array[i] % 2) == 1 and Y == 1) else 0
            flip_probability = math.exp(- self.METASTABLE_BETA * F)
            #print(flip_probability)
            flip_probability *= math.exp(- self.METASTABLE_ALPHA) if X != Y else 1
            #print(str(flip_probability) + " ############")
            if random.random() < flip_probability:  Y_new = -Y

        #print(value_array)
        if X_new == 1 and Y_new == 1:   value_array[0] = 1
        elif X_new == 1 and Y_new == -1:   value_array[0] = 2
        elif X_new == -1 and Y_new == 1:   value_array[0] = 3
        elif X_new == -1 and Y_new == -1:   value_array[0] = 4
        #print(value_array)
        #print("--------------------")
        return value_array
