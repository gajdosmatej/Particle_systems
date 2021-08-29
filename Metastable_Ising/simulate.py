import lattice
import filehandle
import rules
import neighbours

import random
import math
import numpy
import time
import sys

LATTICE_SIDE_LENGTH =20
#LATTICE_SIDE_LENGTH = 15
N_DIM = 3
#MAX_TIME = 200
#STEP_NUM = 1000000
STEP_NUM = 400000
num_of_iter = 1000
initial_law = 1
#initial_law = "diagonal"
#initial_law = "instable_anti"

def getArgsFromCML():
    args = sys.argv
    if len(args) > 1:
        return (float(args[1]), float(args[2]))
    return None

rule = rules.Rules()
neigh = neighbours.Neighbours()

try:
    alpha, beta = getArgsFromCML()
    lat = lattice.Lattice(LATTICE_SIDE_LENGTH, N_DIM, rules.S, initial_law, alpha, beta)
except:
    alpha, beta = None, None
    lat = lattice.Lattice(LATTICE_SIDE_LENGTH, N_DIM, rules.S, initial_law)

N_vertices = pow(lat.side_length, lat.n_dim)

file_handler = filehandle.FileHandler()

rule_map = rule.metastableIsing
neighbour_map = neigh.potts

iter = 1
t = 0
previous_time = time.time()
current_time = 0

for step in range(0, STEP_NUM):
#while(t < MAX_TIME):
    #if t > iter * MAX_TIME / num_of_iter:
    if step > iter * STEP_NUM / num_of_iter:
        current_time = time.time()
        eta = (current_time - previous_time) * (num_of_iter - iter)
        print(str(iter) + " / " + str(num_of_iter) + " | ETA ~ " + str(round(eta,1)) + " s")
        previous_time = time.time()

        file_handler.dumpState(lat.lattice_arr, t)
        iter += 1

    #lat.evolve(neighbour_map, rule_map)
    #t += 1/N_vertices
    t += lat.evolveMetastable()
