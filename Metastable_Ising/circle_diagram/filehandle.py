import json

class FileHandler:
    states_dump_file_name = "./states.txt"
    expected_dump_file_name = "./average.txt"

    def __init__(self):
        f = open(self.states_dump_file_name, "w")
        f.close()
        f = open(self.expected_dump_file_name, "w")
        f.close()

    def dumpState(self, state, time):
        f = open(self.states_dump_file_name, "a")
        state_str = json.dumps(state.tolist())
        f.write(str(time))
        f.write(str(state_str))
        f.write("\n")
        f.close()

    def dumpExpected(self,X,Y,time):
        f = open(self.expected_dump_file_name, "a")
        f.write(str(time))
        f.write(" ")
        f.write(str(X))
        f.write(" ")
        f.write(str(Y))
        f.write("\n")
        f.close()
