import json

class FileHandler:
    states_dump_file_name = "./states.txt"

    def __init__(self):
        f = open(self.states_dump_file_name, "w")
        f.close()

    def dumpState(self, state, time):
        f = open(self.states_dump_file_name, "a")
        state_str = json.dumps(state.tolist())
        f.write(str(time))
        f.write(str(state_str))
        f.write("\n")
        f.close()
