import json
import numpy
import matplotlib
import matplotlib.pyplot

states_dump_file_name = "./states.txt"
parse_num_text = 250

#1 -> X=1;Y=1; 2 -> X=1;Y=-1; 3 -> X=-1;Y=1; 4 -> X=-1;Y=-1
def getExpectedValues(state):
    return numpy.mean(state)

time_list = []
expected_value_list = []

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
    expected_value = getExpectedValues(state)
    expected_value_list.append(expected_value)

    line = f.readline()

#print(time)
fig, ax = matplotlib.pyplot.subplots()
ax.plot(time_list, expected_value_list)

ax.set(xlabel='time [s]', ylabel='expected value',
       title='E(t)')

#ax.grid(which='major', axis='y')
ax.axhline(0, linestyle='solid', color='k')
ax.axhline(1, linestyle='solid', color='k', lw=1)
ax.axhline(-1, linestyle='solid', color='k', lw=1)
fig.savefig("graph_expected.jpg")
matplotlib.pyplot.show()
