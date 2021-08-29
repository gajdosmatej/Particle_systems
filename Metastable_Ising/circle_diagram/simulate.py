import lattice
import filehandle
import calc_circumference
#import rules
#import neighbours

import random
import math
import numpy
import time
import sys

LATTICE_SIDE_LENGTH =30
#LATTICE_SIDE_LENGTH = 15
N_DIM = 3
#MAX_TIME = 200
#STEP_NUM = 1000000
steps_per_print = 200
initial_law = "y0.17"
#initial_law = "diagonal"
#initial_law = "instable_anti"
start_R = 0.17
alpha = None
beta = None

def getArgsFromCML():
    args = sys.argv
    if len(args) > 1:
        return (float(args[1]), float(args[2]), float(args[3]))
    return None

#rule = rules.Rules()
#neigh = neighbours.Neighbours()
S = [1,2,3,4]

def getExpectedValues(state):
    states_X = state[state < 3]
    states_Y = state[state % 2 == 1]

    N_vertex = state.size
    N_X, N_Y = states_X.size, states_Y.size
    return (2*float(N_X) / N_vertex - 1, 2*float(N_Y) / N_vertex - 1)


try:
    alpha, beta, start_r = getArgsFromCML()
    initial_law = "y" + str(start_r)
    start_R = start_r
    lat = lattice.Lattice(LATTICE_SIDE_LENGTH, N_DIM, S, initial_law, alpha, beta)
except:
    alpha, beta = None, None
    lat = lattice.Lattice(LATTICE_SIDE_LENGTH, N_DIM, S, initial_law)

N_vertices = pow(lat.side_length, lat.n_dim)
file_handler = filehandle.FileHandler()



def loop():
    iter_point, iter_print = 1, 1
    t = 0
    step = 0
    start = True
    X_exp, Y_exp = None, None
    Y0 = None

    while True:
        if step == 0:
            (X0, Y0) = getExpectedValues(lat.lattice_arr)

        if step > iter_point * steps_per_print:
            (X_exp, Y_exp) = getExpectedValues(lat.lattice_arr)

            if step > iter_print * 5000:
                print(str(iter_print) + " | " + str(X_exp) + " " + str(Y_exp))
                iter_print += 1

            file_handler.dumpExpected(X_exp, Y_exp, t)

            #if Y_exp < -0.1:	start = False	#pro pocatecni stav (1,1)
            #if (not start) and (Y_exp > -0.02) and (Y_exp < 0.02) and (X_exp > 0): break
            if Y_exp > 0.1: start = False
            if (not start) and (Y_exp <= Y0):   break
            if step > 3000000: break
            iter_point += 1
        #lat.evolve(neighbour_map, rule_map)
        #t += 1/N_vertices
        t += lat.evolveMetastable()
        step += 1
    return X_exp    #polomer na konci


end_r = loop()
while end_r > start_R + 0.03 or end_r < start_R - 0.03:
    print("---------------------")
    print("STARTING RADIUS: " + str(start_R))
    print("RADIUS AFTER CYCLE: " + str(end_r))
    print("---------------------")
    start_R = end_r
    end_r = loop()

print("---------------------")
print("< RADIUS FOUND >")
print(end_r)
print("---------------------")
file_handler = filehandle.FileHandler()
lat = lattice.Lattice(LATTICE_SIDE_LENGTH, N_DIM, S, "y" + str(end_r), alpha, beta)
loop()

circumference = calc_circumference.calcCircumference()
f = open("radii.txt", "a")
f.write(str(alpha) + " " + str(beta) + " " + str(end_r) + " " + str(circumference) + "\n")
