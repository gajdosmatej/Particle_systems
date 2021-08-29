import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy
import json
import math

side_len = 15
T_list = [0.1*i+0.00001 for i in range(0,150)]
my_font = PIL.ImageFont.truetype("/usr/share/fonts/liberation-sans/LiberationSans-Italic.ttf", 34)


def paintCube(row, column, color):
    x,y = column*side_len, row*side_len
    draw.rectangle([(x,y), (x + side_len, y+side_len)], fill=color)



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


def paintState(state):
    lattice_side_length = len(state)    #tohle neni uplne bezpecne - spoleham na to, ze vsechny rozmery jsou stejne
    #print(state)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(state[row][column])
            paintCube(row, column, color)


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
    imgs.append(PIL.Image.new('RGB', (latt_L*side_len, latt_L*side_len+100), color = 'white'))
    draw = PIL.ImageDraw.Draw(imgs[len(imgs)-1])

    state = numpy.array(readState(T))
    paintState(state)
    T_rounded = round(T, 3)
    draw.text((10, (latt_L+2) * side_len), "t = " + str(T_rounded), fill='black', font=my_font)

imgs[0].save('IMGs/animation.gif', save_all=True, append_images=imgs[1:])
