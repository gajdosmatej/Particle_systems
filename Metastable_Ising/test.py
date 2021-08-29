import numpy
import json

VARIABLES = {
    "lattice_length": 7,
    "n_dimensions": 2,
    "end_time": 10
}

class FileHandler:
    states_dump_file_name = "./states.txt"

    def __init__(this):
        f = open(this.states_dump_file_name, "w")
        f.write("t = " + str(VARIABLES["end_time"]) + "\n")
        f.close()

    def dumpState(this, state):
        f = open(this.states_dump_file_name, "a")
        state_str = json.dumps(state.tolist())
        f.write(str(state_str))
        f.write("\n")
        f.close()



def getTensorSizes():
    dimensions_list = [VARIABLES["lattice_length"] for i in range (0, VARIABLES["n_dimensions"])]
    return dimensions_list


def getRandomCoord():
    coord = []

    for dimension in range(0, VARIABLES["n_dimensions"]):
        ran_num = numpy.random.randint(0, VARIABLES["lattice_length"])
        coord.append(ran_num)
    return coord



#vyber souseda je zatim jen testovaci, takhle fungovat nema
def getRandomNeighbour(coord):
    coord[0] = (coord[0] + 1) % VARIABLES["lattice_length"]
    return coord



def updateState(state):
        lattice_coord_list = getRandomCoord()
        neighbour_coord_list = getRandomNeighbour(lattice_coord_list.copy())

        state[tuple(lattice_coord_list)] = state[tuple(neighbour_coord_list)]
        return state


state = numpy.random.randint(0, 2, size=getTensorSizes())
file_handler = FileHandler()

for t in range(0, VARIABLES["end_time"]):
    print("__________________________________ t = " + str(t))
    state = updateState(state)
    file_handler.dumpState(state)
    print(state)
