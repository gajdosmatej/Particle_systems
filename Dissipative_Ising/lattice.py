import numpy
import math
import random

#10.10-11.20
class Lattice:
    side_length = None
    n_dim = None
    lattice_arr = None

    rate_matrix = None
    magnetisation_matrix = None #Metastable Ising
    metastable_alpha = None
    metastable_beta = None
    dissipative_p = None
    dissipative_beta = None
    R_total = None

    def __init__(self, side_length, n_dim, S, initial_law, p=0.5, beta=4):
        self.side_length = side_length
        self.n_dim = n_dim
        self.dissipative_p = p
        self.dissipative_beta = beta

        if initial_law == None:
            self.lattice_arr = self.getInitState(S)
        else:
            self.lattice_arr = numpy.full(shape=self.getLatticeShape(), fill_value=initial_law,dtype=int)

        self.initMagnetisation()    #vypnout, pokud neni metastableIsing
        self.initRates()

    def getInstableInitState(self):
        L = self.side_length
        init_array = numpy.zeros(shape=self.getLatticeShape())
        border = L/2

        for coord in numpy.ndindex(self.getLatticeShape()):
            sum = numpy.sum(list(coord))
            if sum % 2 == 0:
                if coord[0] <= border:   init_array[coord] = 2
                else:   init_array[coord] = 3
            else:
                if coord[0] <= border:   init_array[coord] = 3
                else:   init_array[coord] = 2
        return init_array

    def getDiagonalWaveInitState(self):
        L = self.side_length
        init_array = numpy.zeros(shape=self.getLatticeShape())

        low = L/2
        high = L
        for coord in numpy.ndindex(self.getLatticeShape()):
            sum = numpy.sum(list(coord))
            if sum % 2 == 0:
                if sum < high and sum > low:   init_array[coord] = 1
                elif sum <= low:   init_array[coord] = 2   #tato podminka zpusobuje vznik vlny
                else:   init_array[coord] = 3
            else:
                if sum < high and sum > low:   init_array[coord] = 4
                elif sum <= low:   init_array[coord] = 3
                else:   init_array[coord] = 2
        return init_array

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

    def initMagnetisation(self):
        shape = self.getLatticeShape()
        indices_iterator = numpy.ndindex(shape)
        magnetisation_arr = numpy.zeros(shape)

        for indices in indices_iterator:
            magnetisation_arr[indices] = self.calcMagnetisation(indices)

        self.magnetisation_matrix = magnetisation_arr

    def calcMagnetisation(self, coord):
        local_state = self.lattice_arr[coord]
        local_X, local_Y = self.parseXYFromState(local_state)
        magnetisation = 0

        for neigh_coord in self.neighbourGenerator(coord):
            neigh_X, neigh_Y = self.parseXYFromState(self.lattice_arr[neigh_coord])
            if neigh_X == local_X and neigh_Y == 1:   magnetisation += 1

        return magnetisation

    def calcRate(self, coord):
        magnetisation = self.magnetisation_matrix[coord]
        loc_X,loc_Y = self.parseXYFromState(self.lattice_arr[coord])

        rate = math.exp(-self.dissipative_beta * magnetisation / (self.n_dim*2))
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

    #neni obecne
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
        self.magnetisation_matrix[latt_coord] = self.calcMagnetisation(latt_coord)

        for neigh_coord in self.neighbourGenerator(latt_coord):
            self.magnetisation_matrix[neigh_coord] = self.calcMagnetisation(neigh_coord)

    def neighbourGenerator(self, coord):
        for i in range(0, self.n_dim):
            for modifier in [-1,1]:
                modification_vector = numpy.zeros(self.n_dim, dtype=int)
                modification_vector[i] = modifier
                yield tuple( numpy.mod( numpy.add(numpy.array(coord), modification_vector), self.side_length) )

    def recalculateRates(self, latt_coord):
        self.rate_matrix[latt_coord] = self.calcRate(latt_coord) #index nemuze byt kvuli alpha interakci
        for neigh_coord in self.neighbourGenerator(latt_coord):
            self.rate_matrix[neigh_coord] = self.calcRate(neigh_coord)

    def parseXYFromState(self, state):
        local_X = 1 if state < 3 else -1
        local_Y = 1 if state % 2 == 1 else -1
        return (local_X, local_Y)

    def getStateFromXY(self, X, Y):
        if X == 1 and Y == 1:   return 1
        elif X == 1 and Y == -1:    return 2
        elif X == -1 and Y == 1:    return 3
        elif X == -1 and Y == -1:   return 4
        else: print("ERROR IN LATTICE.GETSTATEFROMXY()")

    def getRandomSite(self):
        coord = []
        for dim in range(0, self.n_dim):
            coord.append(random.randint(0,self.side_length - 1))
        return tuple(coord)

    def evolveDissipative(self):
        site_coord = None
        X,Y = None, None
        if random.random() < self.dissipative_p:
            site_coord = self.getRandomSite()
            X,Y = self.parseXYFromState(self.lattice_arr[site_coord])
            Y = -1
        else:
            site_coord = tuple(self.getSiteFromRates())
            X,Y = self.parseXYFromState(self.lattice_arr[site_coord])
            Y = 1
            X = -X

        new_state = self.getStateFromXY(X, Y)
        self.lattice_arr[site_coord] = new_state

        self.recalculateMagnetisation(site_coord)
        self.recalculateRates(site_coord)    #neni optimalizovane - pocita se X i Y
        self.R_total = numpy.sum(self.rate_matrix)   #tohle bude chtit optimalizovat
        #print(self.R_total)
        return 1/self.R_total

    def evolve(self, neighbour_map, rule_map):
        vertex_coord = numpy.random.randint(self.side_length, size=self.n_dim)
        neighbour_matrix = neighbour_map(vertex_coord, self.n_dim, self.side_length)    #[coord_1 = [...], coord_2 = [...], ...]
        state_array = numpy.array([self.lattice_arr[tuple(coord)] for coord in neighbour_matrix])

        new_state_array = rule_map(state_array) #zda se, ze rule_map primo modifikuje state_array, takze vlastne neni potreba tvorit new_state_array

        self.appendStatesToLattice(new_state_array, neighbour_matrix)
