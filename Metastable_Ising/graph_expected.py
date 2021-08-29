import json
import numpy
import matplotlib
import matplotlib.pyplot

states_dump_file_name = "./states.txt"
parse_num_text = 250

#1 -> X=1;Y=1; 2 -> X=1;Y=-1; 3 -> X=-1;Y=1; 4 -> X=-1;Y=-1
def getExpectedValues(state):
    states_X_1 = state[state < 3]
    states_Y_1 = state[state % 2 == 1]

    N_vertex = state.size
    N_X_1, N_Y_1 = states_X_1.size, states_Y_1.size

    return (2*N_X_1 / N_vertex - 1, 2*N_Y_1 / N_vertex - 1)



time_list = []
expected_value_list_X = []
expected_value_list_Y = []

f = open(states_dump_file_name, "r")
line = f.readline()
line_num, iter = 0, 0

while line != "":
    line_num += 1
    if line_num > iter*parse_num_text:
        print("Parsed " + str(iter*parse_num_text) + " lines")
        iter += 1

    break_index = line.index("[")
    time = line[:break_index]
    json_state = line[break_index:]
    state = numpy.array( json.loads(json_state) )

    time_list.append(float(time))
    expected_values = getExpectedValues(state)
    expected_value_list_X.append(expected_values[0])
    expected_value_list_Y.append(expected_values[1])

    line = f.readline()

#print(time)
fig, ax = matplotlib.pyplot.subplots()
ax.plot(time_list, expected_value_list_X)
ax.plot(time_list, expected_value_list_Y)

ax.set(xlabel='time [s]', ylabel='expected value',
       title='E(t)')

#ax.grid(which='major', axis='y')
ax.axhline(0, linestyle='solid', color='k')
ax.axhline(1, linestyle='solid', color='k', lw=1)
ax.axhline(-1, linestyle='solid', color='k', lw=1)
fig.savefig("graph_expected.jpg")
#matplotlib.pyplot.show()
