import filehandle

import random
import math
import numpy
import time
import sys


LATTICE_SIDE_LENGTH = 20
#LATTICE_SIDE_LENGTH = 15
N_DIM = 3
#MAX_TIME = 200
STEP_NUM = 300000
initial_law = 1


class Lattice:
    side_length = None
    n_dim = None
    lattice_arr = None

    prey_reproduction_rate = 9/10 #sireni prey
    predator_death_rate = 9/10
    spontaneous_change_rate = 1/10000    #na prazdnem poli
    rate_matrix = None
    R_total = None

    def __init__(self, side_length, n_dim, S, initial_law):
        self.side_length = side_length
        self.n_dim = n_dim

        if initial_law == None:
            self.lattice_arr = self.getInitState(S)
        elif initial_law == "wave":
            self.lattice_arr = self.getWaveInitState(S)
        else:
            self.lattice_arr = numpy.full(shape=self.getLatticeShape(), fill_value=initial_law,dtype=int)

        self.initRates()


    def getWaveInitState(self, S):
        S = [1,2,4,3]   #pro spravne zmeny
        states_num = len(S)
        one_state_len = round(self.side_length / states_num)
        remain_len = self.side_length

        init_array = numpy.array([])
        for z in S:
            remain_len -= one_state_len
            arr_shape = [self.side_length for i in range(0, self.n_dim-1)]
            if remain_len >=0:  arr_shape.append(one_state_len)
            else:
                arr_shape.append(one_state_len + remain_len)

            if numpy.size(init_array) == 0:  init_array = numpy.full(shape=tuple(arr_shape), fill_value=z,dtype=int)
            else:   init_array = numpy.append(init_array, numpy.full(shape=tuple(arr_shape), fill_value=z,dtype=int), axis=2)   #neobecne

        if remain_len > 0:
            arr_shape = [self.side_length for i in range(0, self.n_dim-1)]
            arr_shape.append(remain_len)
            init_array = numpy.append(init_array, numpy.full(shape=tuple(arr_shape), fill_value=S[0],dtype=int), axis=2)
        return init_array


    def getNumOfTilesWithState(self, state, coord):
        N = 0
        for neigh_coord in self.neighbourGenerator(coord):
            if self.lattice_arr[neigh_coord] == state: N += 1
        return N


    def calcProbabilityNothingHappens(self, probabilities_list):
        probability = 1
        for i in range(0, len(probabilities_list)):
            probability *= probabilities_list[i]
        return probability


    def calcRate(self, coord):
        state = self.lattice_arr[coord]
        if state == 6:       #prazdno
            #return self.spontaneous_change_rate
            N = self.getNumOfTilesWithState(1, coord)
            return 1 - self.calcProbabilityNothingHappens([self.spontaneous_change_rate] + [self.prey_reproduction_rate for i in range(0, N)])

        elif state == 1:    #korist
            #N = self.getNumOfTilesWithState(6,coord)    #pocet prazdnych policek
            #return 1 - self.calcProbabilityNothingHappens([self.spontaneous_change_rate] + [self.prey_reproduction_rate for i in range(0, N)])
            return self.spontaneous_change_rate

        elif state == 0:    #predator
            N = self.getNumOfTilesWithState(1, coord)   #pocet policek s koristi
            if N == 0:  return 1 - self.calcProbabilityNothingHappens([self.spontaneous_change_rate, self.predator_death_rate])
            else:   return 1    #urcite dojde k presunu


    def initRates(self):
        shape = self.getLatticeShape()
        indices_iterator = numpy.ndindex(shape)

        rates_arr = numpy.zeros(shape)
        for indices in indices_iterator:
            rates_arr[indices] = self.calcRate(indices)

        self.rate_matrix = rates_arr
        self.R_total = numpy.sum(self.rate_matrix)


    def getLatticeShape(self):
        return tuple( self.side_length for i in range(0, self.n_dim) )


    def getInitState(self, S):
        return numpy.random.choice(S, size = self.getLatticeShape())


    def appendStatesToLattice(self, state_array, neighbour_matrix):
        length = len(state_array)
        for vertex_i in range(0, length):
            self.lattice_arr[ tuple(neighbour_matrix[vertex_i]) ] = state_array[vertex_i]


    def getIndexFromProbability(self, probability_law):
        rnd = random.random()
        low, high = 0, 0
        for index in range(0, len(probability_law)):
            high += probability_law[index]
            if rnd > low and rnd <= high:    return index
            low += probability_law[index]


    #neni obecne
    def getSiteFromRates(self):
        x_rates = numpy.sum(numpy.sum(self.rate_matrix, axis = 2), axis = 1)
        R_x = numpy.sum(x_rates)
        x = self.getIndexFromProbability(1/R_x * x_rates)

        y_rates = numpy.sum(self.rate_matrix[x], axis = 1)
        R_y = numpy.sum(y_rates)
        y = self.getIndexFromProbability(1/R_y * y_rates)

        z_rates = self.rate_matrix[x][y]
        R_z = numpy.sum(z_rates)
        z = self.getIndexFromProbability(1/R_z * z_rates)

        return (x,y,z)


    def neighbourGenerator(self, coord):
        for i in range(0, self.n_dim):
            for modifier in [-1,1]:
                modification_vector = numpy.zeros(self.n_dim, dtype=int)
                modification_vector[i] = modifier
                yield tuple( numpy.mod( numpy.add(numpy.array(coord), modification_vector), self.side_length) )


    def recalculateRates(self, latt_coord):
        self.rate_matrix[latt_coord] = self.calcRate(latt_coord)
        for neigh_coord in self.neighbourGenerator(latt_coord):
            self.rate_matrix[neigh_coord] = self.calcRate(neigh_coord)


    def getCoordsFromReproductionNum(self, N_reproduced, site_coord):
        empty_vertices_list = []
        for neigh_coord in self.neighbourGenerator(site_coord):
            if self.lattice_arr[neigh_coord] == 6:  empty_vertices_list.append(neigh_coord)
        indices = random.sample(range(0, N_reproduced), N_reproduced)    #vrati unikatni nahodna cisla v rozpeti
        return [empty_vertices_list[i] for i in range(0, N_reproduced) if i in indices]


    def evolve(self):
        site_coord = self.getSiteFromRates()
        state = self.lattice_arr[site_coord]
        rnd = random.random()

        if state == 6:
            #if rnd < 1/2:   self.lattice_arr[site_coord] = 1
            #else:   self.lattice_arr[site_coord] = 0
            if rnd < self.spontaneous_change_rate:
                if random.random() < 1/2:   self.lattice_arr[site_coord] = 1
                else:   self.lattice_arr[site_coord] = 0
            else:
                self.lattice_arr[site_coord] = 1

        elif state == 1:
            '''
            N = self.getNumOfTilesWithState(6, site_coord)
            if N == 0 or rnd < self.spontaneous_change_rate:
                if random.random() < 1/2:   self.lattice_arr[site_coord] = 0
                else:   self.lattice_arr[site_coord] = 6
            else:
                N_reproduced = random.randint(1, N)
                for neigh_coord in self.getCoordsFromReproductionNum(N_reproduced, site_coord):
                    self.lattice_arr[neigh_coord] = 1
            '''
            if rnd < 1/2:   self.lattice_arr[site_coord] = 0
            else:   self.lattice_arr[site_coord] = 6

        elif state == 0:
            N = self.getNumOfTilesWithState(1, site_coord)
            if rnd < self.spontaneous_change_rate:
                if random.random() < 1/2:   self.lattice_arr[site_coord] = 6
                else:   self.lattice_arr[site_coord] = 1

            if N == 0 and rnd > self.spontaneous_change_rate: #smrt
                self.lattice_arr[site_coord] = 6
            else:
                move_index = self.getIndexFromProbability([1/N for i in range(0, N)])
                j = 0
                for neigh_coord in self.neighbourGenerator(site_coord):
                    if self.lattice_arr[neigh_coord] == 1:
                        if move_index == j:
                            self.lattice_arr[neigh_coord] = 0
                            break
                        j += 1


        self.recalculateRates(site_coord)
        self.R_total = numpy.sum(self.rate_matrix)   #tohle bude chtit optimalizovat
        #print(self.R_total)
        return 1/self.R_total






lat = Lattice(LATTICE_SIDE_LENGTH, N_DIM, [0,1,6], initial_law)
N_vertices = pow(lat.side_length, lat.n_dim)
file_handler = filehandle.FileHandler()

iter = 1
t = 0
previous_time = time.time()
current_time = 0
num_of_iter = 1000

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

    t += lat.evolve()
    #t += 1 / (N_vertices * 2 * math.exp(rule.METASTABLE_BETA+rule.METASTABLE_ALPHA))
    #t += lat.evolveMetastable()
