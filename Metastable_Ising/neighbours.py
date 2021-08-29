import numpy
import random
import math

class Neighbours:
    def voter(self, vertex_coord, n_dim, side_length):   #voter model, contact process
        num_sides = 2*n_dim
        rnd = random.randrange(0, num_sides)
        modification_vector = numpy.zeros(n_dim, dtype=int)   #pole index = 0...n_dim plne nul

        #0 -> [1,0]; 1 -> [-1,0]; 2 -> [0,1]; 3 -> [0,-1]
        index = math.floor(rnd / 2)
        modifier = pow(-1, rnd % 2)

        modification_vector[index] = modifier
        neighbour_coord = numpy.add(vertex_coord, modification_vector)
        neighbour_coord = numpy.mod(neighbour_coord, side_length)   #periodic bounds

        return numpy.array([vertex_coord, neighbour_coord])


    def potts(self, vertex_coord, n_dim, side_length):   #Ising model, Potts model, Metastable Ising model
        num_sides = 2*n_dim
        neighbour_matrix = numpy.array([vertex_coord])

        for i in range(0, n_dim):
            for modifier in [-1,1]:
                modification_vector = numpy.zeros(n_dim, dtype=int)
                modification_vector[i] = modifier
                neighbour_matrix = numpy.append(neighbour_matrix, [numpy.mod( numpy.add(vertex_coord, modification_vector), side_length)] , axis=0 )
        return neighbour_matrix
