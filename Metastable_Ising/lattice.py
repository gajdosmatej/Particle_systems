import numpy
import math
import random

class Lattice:
    side_length = None
    n_dim = None
    lattice_arr = None

    rate_matrix = None
    magnetisation_matrix = None #Metastable Ising
    metastable_alpha = None
    metastable_beta = None
    R_total = None

    def __init__(self, side_length, n_dim, S, initial_law, alpha=1, beta=4):
        self.side_length = side_length
        self.n_dim = n_dim
        self.metastable_alpha = alpha
        self.metastable_beta = beta

        if initial_law == None:
            self.lattice_arr = self.getInitState(S)
        elif initial_law == "wave":
            self.lattice_arr = self.getWaveInitState(S)
        elif initial_law == "diagonal":
            self.lattice_arr = self.getDiagonalWaveInitState()
        elif initial_law == "instable_anti":
            self.lattice_arr = self.getInstableInitState()
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
        shape = list(shape)
        shape.append(2)
        shape = tuple(shape)

        magnetisation_arr = numpy.zeros(shape)

        for indices in indices_iterator:
            magnetisation_arr[indices] = self.calcMagnetisation(indices)

        self.magnetisation_matrix = magnetisation_arr



    def calcMagnetisation(self, coord):
        local_state = self.lattice_arr[coord]
        local_X, local_Y = self.parseXYFromState(local_state)
        magnetisation_X, magnetisation_Y = 0, 0

        for neigh_coord in self.neighbourGenerator(coord):
            neigh_X, neigh_Y = self.parseXYFromState(self.lattice_arr[neigh_coord])
            if neigh_X == local_X:   magnetisation_X += 1
            if neigh_Y == local_Y:  magnetisation_Y += 1

        return (magnetisation_X, magnetisation_Y)


    def calcRate(self, coord, index=None):
        magnetisation_X, magnetisation_Y = self.magnetisation_matrix[coord]
        loc_X,loc_Y = self.parseXYFromState(self.lattice_arr[coord])

        if index != 1:
            rate_X = math.exp(-self.metastable_beta * magnetisation_X / (self.n_dim*2))
            rate_X *= math.exp(-self.metastable_alpha) if loc_X == loc_Y else 1

        if index != 0:
            rate_Y = math.exp(-self.metastable_beta * magnetisation_Y / (self.n_dim*2))
            rate_Y *= math.exp(-self.metastable_alpha) if loc_X != loc_Y else 1

        '''
        rate_X = math.exp(-loc_X * (self.metastable_beta*(2*magnetisation_X - 6)/6 - self.metastable_alpha*loc_Y))
        rate_Y = math.exp(-loc_Y * (self.metastable_beta*(2*magnetisation_Y - 6)/6 + self.metastable_alpha*loc_X))  #metastart
        '''
        '''if index == 1:
            print(self.metastable_beta)
            print(magnetisation_Y)
            print(rate_Y)
            print("-----")'''

        if index == 0:  return rate_X
        elif index == 1:    return rate_Y
        else:   return (rate_X, rate_Y)


    def initRates(self):
        shape = self.getLatticeShape()
        indices_iterator = numpy.ndindex(shape)
        shape = list(shape)
        shape.append(2)
        shape = tuple(shape)

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

        if self.n_dim == 3:
            x_rates = numpy.sum(numpy.sum( numpy.sum(self.rate_matrix, axis = 3), axis = 2), axis = 1)
            R_x = numpy.sum(x_rates)
            x = self.getIndexFromProbability(1/R_x * x_rates)

            y_rates = numpy.sum(numpy.sum(self.rate_matrix[x], axis = 2), axis = 1)
            R_y = numpy.sum(y_rates)
            y = self.getIndexFromProbability(1/R_y * y_rates)

            z_rates = numpy.sum(self.rate_matrix[x][y], axis = 1)
            R_z = numpy.sum(z_rates)
            z = self.getIndexFromProbability(1/R_z * z_rates)

            val_rates = self.rate_matrix[x][y][z]
            R_val = numpy.sum(val_rates)
            val = self.getIndexFromProbability(1/R_val * val_rates)

            return (x,y,z,val)

        elif self.n_dim == 2:
            x_rates = numpy.sum(numpy.sum( self.rate_matrix, axis = 2), axis = 1)
            R_x = numpy.sum(x_rates)
            x = self.getIndexFromProbability(1/R_x * x_rates)

            y_rates = numpy.sum(self.rate_matrix[x], axis = 1)
            R_y = numpy.sum(y_rates)
            y = self.getIndexFromProbability(1/R_y * y_rates)

            val_rates = self.rate_matrix[x][y]
            R_val = numpy.sum(val_rates)
            val = self.getIndexFromProbability(1/R_val * val_rates)

            return (x,y,val)


    def recalculateMagnetisation(self, latt_coord, index):
        self.magnetisation_matrix[latt_coord][index] = 2*self.n_dim - self.magnetisation_matrix[latt_coord][index]
        new_local_states = self.parseXYFromState(self.lattice_arr[latt_coord])

        for neigh_coord in self.neighbourGenerator(latt_coord):
                if new_local_states[index] == self.parseXYFromState(self.lattice_arr[neigh_coord])[index]:
                    self.magnetisation_matrix[neigh_coord][index] += 1
                else: self.magnetisation_matrix[neigh_coord][index] += -1


    def neighbourGenerator(self, coord):
        for i in range(0, self.n_dim):
            for modifier in [-1,1]:
                modification_vector = numpy.zeros(self.n_dim, dtype=int)
                modification_vector[i] = modifier
                yield tuple( numpy.mod( numpy.add(numpy.array(coord), modification_vector), self.side_length) )


    def recalculateRates(self, latt_coord, index):
        self.rate_matrix[latt_coord] = self.calcRate(latt_coord) #index nemuze byt kvuli alpha interakci
        for neigh_coord in self.neighbourGenerator(latt_coord):
            self.rate_matrix[neigh_coord][index] = self.calcRate(neigh_coord, index)


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


    def evolveMetastable(self):
        site_coord = self.getSiteFromRates()    # n_D + 1
        lattice_coord = tuple(site_coord[:-1])
        is_Y = site_coord[-1]

        X,Y = self.parseXYFromState(self.lattice_arr[lattice_coord])
        if is_Y == 0:    X = -X
        else:   Y = -Y
        new_state = self.getStateFromXY(X, Y)
        self.lattice_arr[lattice_coord] = new_state

        self.recalculateMagnetisation(lattice_coord, is_Y)
        self.recalculateRates(lattice_coord, is_Y)    #neni optimalizovane - pocita se X i Y
        self.R_total = numpy.sum(self.rate_matrix)   #tohle bude chtit optimalizovat
        #print(self.R_total)
        return 1/self.R_total


    def evolve(self, neighbour_map, rule_map):
        vertex_coord = numpy.random.randint(self.side_length, size=self.n_dim)
        neighbour_matrix = neighbour_map(vertex_coord, self.n_dim, self.side_length)    #[coord_1 = [...], coord_2 = [...], ...]
        state_array = numpy.array([self.lattice_arr[tuple(coord)] for coord in neighbour_matrix])

        new_state_array = rule_map(state_array) #zda se, ze rule_map primo modifikuje state_array, takze vlastne neni potreba tvorit new_state_array

        self.appendStatesToLattice(new_state_array, neighbour_matrix)
