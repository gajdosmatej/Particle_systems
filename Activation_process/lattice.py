import numpy
import math
import random

#1 -> ready
#2 -> activated
#0 -> charging
#22.7.2021 11.15 - 11.34

class Lattice:
    side_length = None
    n_dim = None
    lattice_arr = None

    rate_matrix = None
    N2_matrix = None
    N0_matrix = None
    activation_k = None
    activation_nu = None
    activation_c = None
    R_total = None

    def __init__(self, side_length, n_dim, S, initial_law, k=1, nu=1, c=1):
        self.side_length = side_length
        self.n_dim = n_dim
        self.activation_k = k
        self.activation_nu = nu
        self.activation_c = c

        if initial_law == None:
            self.lattice_arr = self.getInitState(S)
        else:
            self.lattice_arr = numpy.full(shape=self.getLatticeShape(), fill_value=initial_law,dtype=int)

        self.initMagnetisation()
        self.initRates()

    def initMagnetisation(self):
        shape = self.getLatticeShape()
        indices_iterator = numpy.ndindex(shape)
        N2_arr = numpy.zeros(shape)
        N0_arr = numpy.zeros(shape)

        for indices in indices_iterator:
            N2_arr[indices] = self.calcMagnetisation(indices, 2)
            N0_arr[indices] = self.calcMagnetisation(indices, 0)

        self.N2_matrix = N2_arr
        self.N0_matrix = N0_arr

    def calcMagnetisation(self, coord, val):
        local_state = self.lattice_arr[coord]
        magnetisation = 0

        for neigh_coord in self.neighbourGenerator(coord):
            neigh_state = self.lattice_arr[neigh_coord]
            if neigh_state == val:   magnetisation += 1

        return magnetisation

    def calcRate(self, coord):
        local_state = self.lattice_arr[coord]
        rate = None

        if local_state == 1:
            N2 = self.N2_matrix[coord]
            N0 = self.N0_matrix[coord]

            #rate = self.activation_k * N2
            #rate += 0.0001 if N0 == 0 else 0
            rate = math.exp(self.activation_k*N2)

        elif local_state == 2:
            rate = self.activation_nu
        else:   #spoleham, ze jsou mozne jen hodnoty {0,1,2}
            rate = self.activation_c
        return rate

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
        for index in range(0,probability_law.size):
            high += probability_law[index]
            if rnd > low and rnd <= high:    return index
            low += probability_law[index]

    def getSiteFromRates(self):

        if self.n_dim == 3:
            x_rates = numpy.sum( numpy.sum(self.rate_matrix, axis = 2), axis = 1)
            R_x = numpy.sum(x_rates)
            x = self.getIndexFromProbability(1/R_x * x_rates)

            y_rates = numpy.sum(self.rate_matrix[x], axis = 1)
            R_y = numpy.sum(y_rates)
            y = self.getIndexFromProbability(1/R_y * y_rates)

            z_rates = self.rate_matrix[x][y]
            R_z = numpy.sum(z_rates)
            z = self.getIndexFromProbability(1/R_z * z_rates)

            return (x,y,z)

        elif self.n_dim == 2:
            x_rates = numpy.sum(self.rate_matrix, axis = 1)
            R_x = numpy.sum(x_rates)
            x = self.getIndexFromProbability(1/R_x * x_rates)

            y_rates = self.rate_matrix[x]
            R_y = numpy.sum(y_rates)
            y = self.getIndexFromProbability(1/R_y * y_rates)

            return (x,y)

    def recalculateMagnetisation(self, latt_coord):
        self.N2_matrix[latt_coord] = self.calcMagnetisation(latt_coord, 2)
        self.N0_matrix[latt_coord] = self.calcMagnetisation(latt_coord, 0)

        for neigh_coord in self.neighbourGenerator(latt_coord):
            self.N2_matrix[neigh_coord] = self.calcMagnetisation(neigh_coord,2)
            self.N0_matrix[neigh_coord] = self.calcMagnetisation(neigh_coord, 0)

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

    def getRandomSite(self):
        coord = []
        for dim in range(0, self.n_dim):
            coord.append(random.randint(0,self.side_length - 1))
        return tuple(coord)

    def evolveActivation(self):
        site_coord = tuple(self.getSiteFromRates())
        state = self.lattice_arr[site_coord]

        new_state = (state+1) % 3
        self.lattice_arr[site_coord] = new_state

        self.recalculateMagnetisation(site_coord)
        self.recalculateRates(site_coord)
        self.R_total = numpy.sum(self.rate_matrix)   #tohle bude chtit optimalizovat
        return 1/self.R_total

    def evolve(self, neighbour_map, rule_map):
        vertex_coord = numpy.random.randint(self.side_length, size=self.n_dim)
        neighbour_matrix = neighbour_map(vertex_coord, self.n_dim, self.side_length)    #[coord_1 = [...], coord_2 = [...], ...]
        state_array = numpy.array([self.lattice_arr[tuple(coord)] for coord in neighbour_matrix])

        new_state_array = rule_map(state_array) #zda se, ze rule_map primo modifikuje state_array, takze vlastne neni potreba tvorit new_state_array

        self.appendStatesToLattice(new_state_array, neighbour_matrix)
