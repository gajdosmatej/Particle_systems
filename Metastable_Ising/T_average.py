import json
import numpy
import sys

states_dump_file_name = "./states.txt"
parse_num_text = 250

#1 -> X=1;Y=1; 2 -> X=1;Y=-1; 3 -> X=-1;Y=1; 4 -> X=-1;Y=-1
def getExpectedValues(state):
    states_X_1 = state[state < 3]
    states_Y_1 = state[state % 2 == 1]

    N_vertex = state.size
    N_X_1, N_Y_1 = states_X_1.size, states_Y_1.size

    return (2*N_X_1 / N_vertex - 1, 2*N_Y_1 / N_vertex - 1)



args = sys.argv
alpha, beta = float(args[1]), float(args[2])

f = open(states_dump_file_name, "r")
line = f.readline()
line_num, iter = 0, 0
X_pivot, Y_pivot = None, None
X_already, Y_already = False, False
T_list = numpy.array([])
step_list = numpy.array([])
X_step_pivot, Y_step_pivot = None, None

while line != "":
    line_num += 1
    if line_num > iter*parse_num_text:
        print("Parsed " + str(iter*parse_num_text) + " lines")
        iter += 1

    break_index = line.index("[")
    time = float(line[:break_index])
    json_state = line[break_index:]
    state = numpy.array( json.loads(json_state) )

    expected_X, expected_Y = getExpectedValues(state)
    if expected_X > -0.1 and expected_X < 0.1 and not X_already:
        X_already = True
        if X_pivot != None:
            T_list = numpy.append(T_list, time - X_pivot)
        X_pivot = time
        if X_step_pivot != None:
            step_list = numpy.append(step_list, line_num - X_step_pivot)
        X_step_pivot = line_num

    elif X_already and (expected_X < -0.1 or expected_X > 0.1):
        X_already = False

    if expected_Y > -0.1 and expected_Y < 0.1 and not Y_already:
        Y_already = True
        if Y_pivot != None:
            T_list = numpy.append(T_list, time - Y_pivot)
        Y_pivot = time
        if Y_step_pivot != None:
            step_list = numpy.append(step_list, line_num - Y_step_pivot)
        Y_step_pivot = line_num

    elif Y_already and (expected_Y < -0.1 or expected_Y > 0.1):
        Y_already = False

    line = f.readline()

f.close()
T = round(2*numpy.mean(T_list),2)
step_T = round(2*1000*numpy.mean(step_list), 2) #kvuli num_of_iter

f = open("perioda.txt", "a")
f.write(str(alpha) + " " + str(beta) + " " + str(T) + " " + str(step_T) + "\n")
f.close()
