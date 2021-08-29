import json
import numpy
import math
import matplotlib
import matplotlib.pyplot

states_dump_file_name = "./average.txt"
parse_num_text = 250

#1 -> X=1;Y=1; 2 -> X=1;Y=-1; 3 -> X=-1;Y=1; 4 -> X=-1;Y=-1
def getExpectedValues(state):
    states_X_1 = state[state < 3]
    states_Y_1 = state[state % 2 == 1]

    N_vertex = state.size
    N_X_1, N_Y_1 = states_X_1.size, states_Y_1.size

    return (2*N_X_1 / N_vertex - 1, 2*N_Y_1 / N_vertex - 1)

def calcCirc(X_list, Y_list):
    o = 0
    for i in range(1, len(X_list)):
        o += math.sqrt(pow((X_list[i] - X_list[i-1]), 2) + pow((Y_list[i] - Y_list[i-1]), 2))
    return o

X_list = []
Y_list = []

f = open(states_dump_file_name, "r")
line = f.readline()
line_num, iter = 0, 0

while line != "":
    line_num += 1
    if line_num > iter*parse_num_text:
        print("Parsed " + str(iter*parse_num_text) + " lines")
        iter += 1

    break_index = line.index(" ")
    time = line[:break_index]
    vals = line[break_index+1:]

    break_index = vals.index(" ")
    X = float(vals[:break_index])
    Y = float(vals[break_index+1:])

    X_list.append(X)
    Y_list.append(Y)

    line = f.readline()

o = round(calcCirc(X_list, Y_list),2)
#print(time)
fig, ax = matplotlib.pyplot.subplots()
ax.plot(X_list, Y_list)
matplotlib.pyplot.text(1.2,1.1,"o = " + str(o), bbox = dict(facecolor = 'blue', alpha = 0.2))
ax.set(xlabel='X', ylabel='Y',
       title='Pruchod stavovym prostorem mrizky v case')
matplotlib.pyplot.xlim([-1, 1])
matplotlib.pyplot.ylim([-1, 1])
ax.grid(which='major')
#ax.axis('equal')
matplotlib.pyplot.gca().set_aspect('equal', adjustable='box')
fig.savefig("circle.jpg")
#matplotlib.pyplot.show()
