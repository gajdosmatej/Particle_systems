import numpy
import json
import sys


def getArgsFromCML():
    args = sys.argv
    return (float(args[1]), float(args[2]))


def getExpectedValues(state):
    states_X_1 = state[state < 3]
    states_Y_1 = state[state % 2 == 1]

    N_vertex = state.size
    N_X_1, N_Y_1 = states_X_1.size, states_Y_1.size

    return (2*N_X_1 / N_vertex - 1, 2*N_Y_1 / N_vertex - 1)

def getRowExpectedValue(state, row, L):
    vals = []
    for col in range(0, L):
        vals.append(state[row][col][0])
    return numpy.mean(vals)


def getDeviation(state):
    L = numpy.shape(state)[0]
    row_expected_values = []
    for row in range(0, L):
        row_expected_values.append( getRowExpectedValue(state, row, L) )
    return numpy.std(row_expected_values)


time = 0
expected_value_list_X = []
expected_value_list_Y = []
expected_list_maximum_X = []
expected_list_maximum_Y = []
is_increasing_X, is_increasing_Y = False, False
temp_expected_vaules_X = []
temp_expected_vaules_Y = []
time_list_vertex_change = []
deviations = []

f = open("states.txt", "r")
line = f.readline()
line_num, iter = 0, 0

while line != "":
    line_num += 1
    if line_num > iter*250:
        print("Parsed " + str(iter*250) + " lines")
        iter += 1

    break_index = line.index("[")
    time = line[:break_index]
    json_state = line[break_index:]
    state = numpy.array( json.loads(json_state) )
    deviations.append( getDeviation(state) )


    expected_values = getExpectedValues(state)
    list_L = len(expected_value_list_X)
    '''if list_L != 0:
        if (not is_increasing_X) and (expected_values[0] > expected_value_list_X[list_L-1]):  is_increasing_X = True
        if (is_increasing_X) and (expected_values[0] < expected_value_list_X[list_L-1]):
            is_increasing_X = False
            expected_list_maximum_X.append(expected_values[0])


        if (not is_increasing_Y) and (expected_values[1] > expected_value_list_Y[list_L-1]):  is_increasing_Y = True
        if (is_increasing_Y) and (expected_values[1] < expected_value_list_Y[list_L-1]):
            is_increasing_Y = False
            expected_list_maximum_Y.append(expected_values[1])'''

    temp_expected_vaules_X.append(expected_values[0])
    temp_expected_vaules_Y.append(expected_values[1])

    expected_value_list_X.append(expected_values[0])
    expected_value_list_Y.append(expected_values[1])

    if expected_values[0] < 0.05 and expected_values[0] > -0.05:
        max = numpy.max(numpy.array(temp_expected_vaules_X))
        min = numpy.min(numpy.array(temp_expected_vaules_X))
        if max > abs(min):   expected_list_maximum_X.append(max)
        temp_expected_vaules_X = []

    if expected_values[1] < 0.05 and expected_values[1] > -0.05:
        max = numpy.max(numpy.array(temp_expected_vaules_Y))
        min = numpy.min(numpy.array(temp_expected_vaules_Y))
        if max > abs(min):   expected_list_maximum_Y.append(max)
        temp_expected_vaules_Y = []

    line = f.readline()

f.close()

mean_E_X = numpy.mean(numpy.array(expected_value_list_X))
mean_E_Y = numpy.mean(numpy.array(expected_value_list_Y))
mean_deviation = numpy.mean(numpy.array(deviations))

if len(expected_list_maximum_X) == 0:   mean_E_max_X = 10*mean_E_X / abs(mean_E_X)
else:   mean_E_max_X = numpy.mean(numpy.array(expected_list_maximum_X[1:])) #filtr konstantniho rozdeleni

if len(expected_list_maximum_Y) == 0:   mean_E_max_Y = 10*mean_E_Y / abs(mean_E_Y)
else:   mean_E_max_Y = numpy.mean(numpy.array(expected_list_maximum_Y[1:]))

alpha, beta = getArgsFromCML()

f = open("./expected_values.txt", "a")
#f.write("alpha beta mean_E_X mean_E_Y mean_E_max_X mean_E_max_Y time\n")
f.write(str(alpha) + " " + str(beta) + " " + str(mean_E_X) + " " + str(mean_E_Y) + " " + str(mean_E_max_X) + " " + str(mean_E_max_Y) + " " + str(time) + " " + str(mean_deviation) + "\n")
f.close()
