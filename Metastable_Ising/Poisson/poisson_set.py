import random
import matplotlib.pyplot
import math

def floatRangeGenerator(a, b, step):
    i = a
    while i < b:
        yield i
        i += step

def isNumChosen(epsilon, r):
    probability = epsilon * epsilon * r
    if random.random() < probability:   return True
    return False

def sum(list, last_index):
    U = 0
    for i in range(0, last_index):
        U += list[i]
    return U


a, b = 0, 500
epsilon = 1/170
r = 3

Z_epsilon = [ (z_epsilon_x,z_epsilon_y) for z_epsilon_x in floatRangeGenerator(a*epsilon, b*epsilon, epsilon)
                for z_epsilon_y in floatRangeGenerator(a*epsilon, b*epsilon, epsilon)]

PI_epsilon = [pi_epsilon for pi_epsilon in Z_epsilon if isNumChosen(epsilon, r)]


matplotlib.pyplot.scatter( [x[0] for x in PI_epsilon], [y[1] for y in PI_epsilon] )
matplotlib.pyplot.show()

lamb = 3
max = 20
T = [- lamb * math.log(random.random()) for i in range(0,max)]
sums = [sum(T,i) for i in range(0,max)]

matplotlib.pyplot.scatter(sums, [0 for i in range(0, max)])
matplotlib.pyplot.show()
