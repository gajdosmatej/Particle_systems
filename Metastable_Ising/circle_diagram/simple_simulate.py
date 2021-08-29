#21.7.2021 10.00 -11.05
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
steps_per_print = 1000
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
    iter = 1
    t = 0
    step = 0
    start = True
    X_exp, Y_exp = None, None

    while True:
        if step > iter * steps_per_print:
            (X_exp, Y_exp) = getExpectedValues(lat.lattice_arr)

            print(str(iter) + " | " + str(X_exp) + " " + str(Y_exp))
            file_handler.dumpExpected(X_exp, Y_exp, t)

            if Y_exp < -0.1:	start = False	#pro pocatecni stav (1,1)
            if (not start) and (Y_exp > -0.03) and (Y_exp < 0.03) and (X_exp > 0): break
            if step > 200000: break
            iter += 1
        #lat.evolve(neighbour_map, rule_map)
        #t += 1/N_vertices
        t += lat.evolveMetastable()
        step += 1
    return X_exp    #polomer na konci

loop()
print("Loop 1 completed")
loop()
