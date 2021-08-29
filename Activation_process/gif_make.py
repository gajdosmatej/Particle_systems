import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy
import json

side_len = 15
T_list = [0.00020*i+0.00005 for i in range(0,200)]
my_font = PIL.ImageFont.truetype("/usr/share/fonts/liberation-sans/LiberationSans-Italic.ttf", 34)


def paintCube(row, column, color):
    x,y = column*side_len, row*side_len
    draw.rectangle([(x,y), (x + side_len, y+side_len)], fill=color)


def collapseHigherDimensions(state, axis):
    if axis == 0:   return state[0]
    elif axis == 1: return state[:,len(state)-1]
    elif axis == 2: return state[:,:,len(state)-1]
    else:   print("Undefined behaviour")


def chooseColor(val):
    if val == 0: return "#3f3f4d"    #grey
    elif val == 1: return "#5757f6" #blue
    elif val == 2: return "#d9d900" #yellow
    elif val == 3: return "#red"
    elif val == 4: return "#000099"
    elif val == -1: return "orange"
    elif val == 5: return "cyan"
    elif val == 6: return "gray"
    else: return "black"

def initLanes(lattice_len):
    whole_side_len = side_len*lattice_len
    draw.line([(0, whole_side_len), (whole_side_len, whole_side_len)], fill="black", width=4)
    draw.line([(whole_side_len, 0), (whole_side_len, whole_side_len)], fill="black", width=4)


def paintState(state):
    lattice_side_length = len(state)    #tohle neni uplne bezpecne - spoleham na to, ze vsechny rozmery jsou stejne
    sub_state = collapseHigherDimensions(state,0)
    #print(state)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(row, column, color)

    sub_state = collapseHigherDimensions(state,1)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(row+lattice_side_length, column, color)

    sub_state = collapseHigherDimensions(state,2)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(column, row+lattice_side_length, color)
    initLanes(len(state))


def initFile():
    states_dump_file_name = "./states.txt"
    global f
    f = open(states_dump_file_name, "r")
    line = f.readline()
    break_index = line.index("[")
    return json.loads(line[break_index:])


def readState(T_m):
    time = 0
    while time < T_m:
        line = f.readline()
        if line == "":
            return []
        else:
            break_index = line.index("[")
            time = float(line[:break_index])

    return json.loads(line[break_index:])

def closeFile():
    global f
    f.close()
    f = None


latt_L = len(initFile())

imgs = []
for T in T_list:
    imgs.append(PIL.Image.new('RGB', (latt_L*side_len*2, latt_L*side_len*2), color = 'white'))
    draw = PIL.ImageDraw.Draw(imgs[len(imgs)-1])

    state = numpy.array(readState(T))
    paintState(state)
    draw.text(((latt_L+2) * side_len, (latt_L+2) * side_len), "t = " + str(T), fill='black', font=my_font)

imgs[0].save('animation.gif', save_all=True, append_images=imgs[1:])
