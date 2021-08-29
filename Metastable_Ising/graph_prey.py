import json
import numpy
import matplotlib
import matplotlib.pyplot

states_dump_file_name = "./states.txt"
parse_num_text = 250

def getExpectedValues(state):
    prey_l = state[state == 1]
    predator_l = state[state == 0]

    N_vertex = state.size
    prey_s, predator_s = prey_l.size, predator_l.size

    return (prey_s / N_vertex, predator_s / N_vertex)


time_list = []
prey_list = []
predator_list = []
death_list = []

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
    prey_list.append(expected_values[0])
    predator_list.append(expected_values[1])
    death_list.append(1 - expected_values[0] - expected_values[1])

    line = f.readline()

#print(time)
fig, ax = matplotlib.pyplot.subplots()
ax.plot(time_list, prey_list)
ax.plot(time_list, predator_list)
ax.plot(time_list, death_list, color="gray")

ax.set(xlabel='time [s]', ylabel='ratio',
       title='R(t)')

#ax.grid(which='major', axis='y')
matplotlib.pyplot.show()
fig.savefig("graph_prey.jpg")
