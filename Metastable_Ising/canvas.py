import tkinter
import json
import numpy

side_len = None
f = None
canvas_len = 650

def initFile():
    states_dump_file_name = "./states.txt"
    global f
    f = open(states_dump_file_name, "r")
    line = f.readline()
    break_index = line.index("[")
    return json.loads(line[break_index:])


def readState(buttonStep, step_T = 1):
    for i in range(1, step_T):  f.readline()
    line = f.readline()
    if line == "":
        buttonStep["state"] = "disabled"
        return []
    else:
        break_index = line.index("[")
        time = line[:break_index]
        json_state = line[break_index:]
        return (time, json.loads(json_state) )

def closeFile():
    global f
    f.close()
    f = None


def paintCube(row, column, canvas, color):
    x_begin = column*side_len
    y_begin = row*side_len
    x_end = x_begin + side_len
    y_end = y_begin + side_len
    canvas.create_rectangle(x_begin, y_begin, x_end, y_end, fill=color)


def collapseHigherDimensions(state, axis):
    if axis == 0:   return state[0]
    elif axis == 1: return state[:,len(state)-1]
    elif axis == 2: return state[:,:,len(state)-1]  #aby steny odpovidaly
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


#nyni jen 3d
def paintState(state, canvas):
    lattice_side_length = len(state)    #tohle neni uplne bezpecne - spoleham na to, ze vsechny rozmery jsou stejne
    sub_state = collapseHigherDimensions(state,0)

    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(row, column, canvas, color)

    sub_state = collapseHigherDimensions(state,1)

    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(row+lattice_side_length, column, canvas, color)

    sub_state = collapseHigherDimensions(state,2)
    for row in range(0, lattice_side_length):
        for column in range(0, lattice_side_length):
            color = chooseColor(sub_state[row][column])
            paintCube(column, row+lattice_side_length, canvas, color) #aby steny odpovidaly
    initLanes(len(state))


def textWidgetOverwrite(widget, text):
    widget.delete(0.0, tkinter.END)
    widget.insert(tkinter.END, text)


def step(canvas, button):
    step_T = int(textStep.get(1.0, tkinter.END))
    state_info = readState(button, step_T)
    state = numpy.array(state_info[1])
    textWidgetOverwrite(textTime, "t = " + state_info[0])


    if state.size != 0:
        canvas.delete("all")
        paintState(state, canvas)


def flow(tkApp, canvas, button):
    #button["state"] = "disabled"
    state_info = readState(button)
    state = numpy.array(state_info[1])
    textWidgetOverwrite(textTime, "t = " + state_info[0])

    if state.size != 0:
        canvas.delete("all")
        paintState(state, canvas)
        tkApp.after(10, lambda: flow(tkApp,canvas,button))


def reset():
    closeFile()
    initFile()
    textWidgetOverwrite(textTime, "t = 0")
    initCanvas()
    buttonStep["state"] = "normal"
    buttonFlow["state"] = "normal"

def initLanes(state_len):
    whole_side_len = state_len*side_len
    canvas.create_line(whole_side_len, 0, whole_side_len, whole_side_len, width=4)
    canvas.create_line(0, whole_side_len, whole_side_len, whole_side_len, width=4)


def initCanvas():
    state_info = readState(buttonStep)
    state = numpy.array(state_info[1])
    textWidgetOverwrite(textTime, "t = " + state_info[0])
    paintState(state, canvas)


lattice_L = len(initFile())
side_len = canvas_len // (2*lattice_L)

top = tkinter.Tk()
top.attributes('-zoomed', True)

canvas = tkinter.Canvas(top, bg="white", height=canvas_len, width=canvas_len)

buttonStep = tkinter.Button(top, text="Step", command= lambda: step(canvas, buttonStep))
buttonStep.pack()

buttonFlow = tkinter.Button(top, text="Flow", command= lambda: flow(top, canvas, buttonFlow))
buttonFlow.pack()

buttonReset = tkinter.Button(top, text="Reset", command= lambda: reset())
buttonReset.pack()

textTime = tkinter.Text(top, height = 1, width = 25)
textTime.bind("<Key>", lambda e: "break")   #read-only
textTime.pack()

textStep = tkinter.Text(top, height = 1, width = 25)
textStep.insert(tkinter.END, "1")
textStep.pack()

initCanvas()

canvas.pack()

top.mainloop()
