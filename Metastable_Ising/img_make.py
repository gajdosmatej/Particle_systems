import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy
import json

side_len = 7
my_font = PIL.ImageFont.truetype("/usr/share/fonts/liberation-sans/LiberationSans-Italic.ttf", 25)


def paintCube(row, column, color):
    x,y = column*side_len, row*side_len
    draw.rectangle([(x,y), (x + side_len, y+side_len)], fill=color)


def collapseHigherDimensions(state, axis):
    if axis == 0:   return state[0]
    elif axis == 1: return state[:,len(state)-1]
    elif axis == 2: return state[:,:,len(state)-1]
    else:   print("Undefined behaviour")


def chooseColor(val):
    if val == 0: return "red"
    elif val == 1: return "#FFAA00"
    elif val == 2: return "#0000FF"
    elif val == 3: return "#996600"
    elif val == 4: return "#000099"
    elif val == -1: return "orange"
    elif val == 5: return "cyan"
    elif val == 6: return "gray"
    else: return "black"

def initLanes(lattice_len, row0, column0):
    whole_side_len = side_len*lattice_len
    x0 = column0 * side_len
    y0 = row0 * side_len
    draw.line([(x0, y0+whole_side_len), (x0+whole_side_len, y0+whole_side_len)], fill="black", width=4)
    draw.line([(x0 + whole_side_len, y0), (x0+whole_side_len, y0+whole_side_len)], fill="black", width=4)


def paintState(state, row0, column0):
    lattice_side_length = len(state)    #tohle neni uplne bezpecne - spoleham na to, ze vsechny rozmery jsou stejne
    sub_state = collapseHigherDimensions(state,0)
    #print(state)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(row0 + row, column0 + column, color)

    sub_state = collapseHigherDimensions(state,1)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(row0 + row+lattice_side_length, column0 + column, color)

    sub_state = collapseHigherDimensions(state,2)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(row0 + column, column0 + row+lattice_side_length, color)
    initLanes(len(state), row0, column0)


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

img = PIL.Image.new('RGB', (latt_L*side_len*2*3+12*side_len, latt_L*side_len*2), color = 'white')
draw = PIL.ImageDraw.Draw(img)
T_list = [0.01, 0.05, 0.1]

for i in [0,1,2]:
    state = numpy.array(readState(T_list[i]))
    paintState(state, 0, 2*i*(latt_L+3))
    draw.text((2*i*(latt_L+3) * side_len + latt_L*side_len + 30, (latt_L+2) * side_len), "t = " + str(T_list[i]), fill='black', font=my_font)

img.save('IMGs/evolution.png')
