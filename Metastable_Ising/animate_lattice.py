import json
import numpy
import matplotlib
import matplotlib.pyplot
import matplotlib.widgets

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


def readState(step_T = 1):
    for i in range(1, step_T):  f.readline()
    line = f.readline()
    if line == "":
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
    elif val == 1: return "blue"
    elif val == 2: return "yellow"
    elif val == 3: return "green"
    elif val == 4: return "purple"
    elif val == -1: return "orange"
    elif val == 5: return "cyan"
    else: return "black"


#nyni jen 3d
COLOURS = ["blue","yellow","green","purple"]
def paintState(state):
    lattice_side_length = len(state)    #tohle neni uplne bezpecne - spoleham na to, ze vsechny rozmery jsou stejne
    sub_state = collapseHigherDimensions(state,0)

    for colour in range(1,5):
        indices = numpy.where(state == colour)

            #state[filtered_state[0][i],filtered_state[1][i],filtered_state[2][i]]

        xs = indices[0]
        ys = indices[1]
        zs = indices[2]
        ax.scatter(xs, ys, zs, marker="o", color=COLOURS[colour-1])


def textWidgetOverwrite(widget, text):
    widget.delete(0.0, tkinter.END)
    widget.insert(tkinter.END, text)


def step(arg):
    #step_T = int(textStep.get(1.0, tkinter.END))
    step_T = 1
    state_info = readState(step_T)
    state = numpy.array(state_info[1])

    if state.size != 0:
        paintState(state)


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



lattice_L = len(initFile())
side_len = canvas_len // (2*lattice_L)
'''
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
'''

fig = matplotlib.pyplot.figure()
ax = fig.add_subplot(projection='3d')

'''
xs = numpy.linspace(0,0,5)
ys = numpy.linspace(10,20,5)
zs = numpy.linspace(10,20,5)
ax.scatter(xs, ys, zs, marker="o")
'''

axnext = matplotlib.pyplot.axes([0.81, 0.05, 0.1, 0.075])
ButtonStart = matplotlib.widgets.Button(axnext, 'Next')
ButtonStart.on_clicked(step)
matplotlib.pyplot.show()
