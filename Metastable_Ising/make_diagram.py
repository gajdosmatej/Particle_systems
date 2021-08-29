import matplotlib
import matplotlib.pyplot
import numpy
import math

def parseLine():
    line = f.readline()
    break_index = line.find(" ")
    parsed_list = []
    while break_index != -1:
        parsed_list.append(float(line[:break_index]))
        line = line[break_index+1:]
        break_index = line.find(" ")

    if len(line) != 0:
        parsed_list.append(float(line))
        return parsed_list
    else:   return None

def findTresholdValues(data, alphas, rule):
    alpha_list = []
    treshold_values = []

    for alpha in alphas:
        temp = data[(data[:,0] == alpha)]
        temp = temp[rule(temp),1]  #pravidlo posuzuje na zaklade nejakeho sloupce; nove temp jen betas
        #print(temp)
        if temp.size != 0:
            alpha_list.append(alpha)
            treshold_values.append(temp.min())
    return alpha_list, treshold_values


def ruleConstant(data_list):
    return ( abs(data_list[:,2]) > 0.8 )

def rulePartiallyPeriodic(data_list):
    return (data_list[:,4] > 0.3)   #abs neni, protoze v datech jsou amplitudy maxim

def ruleFullyPeriodic(data_list):
    return (data_list[:,4] > 0.9)

def ruleWaves(data_list):
    return (data_list[:,7] < 0.12)


f = open("./expected_values.txt", "r")
f.readline()    #1. radek

fig, ax = matplotlib.pyplot.subplots()

ax.set_xlabel(r"$\alpha$",fontsize=12)
ax.set_ylabel(r"$\beta$", fontsize=12)
ax.set_title("Fazovy diagram - Metastable Ising Model")
ax.set_xlim([-3.5,3.5])
ax.set_ylim([1,13])


data = numpy.array([])

data_line = parseLine()
while data_line != None:
    data = numpy.append(data, data_line)
    #matplotlib.pyplot.scatter(data_line[0], data_line[1],c="red")
    data_line = parseLine()

data = numpy.reshape(data, (-1,8))  #radek ma 8 polozek

#hranice nahodne - periodicke
alpha_list, values = findTresholdValues(data, numpy.arange(-4, 3.75, 0.125), rulePartiallyPeriodic)
matplotlib.pyplot.scatter(alpha_list, values, marker="x", c="#15328e", label="Zacatek periodicnosti (E[A] > 0.3)")
matplotlib.pyplot.plot(alpha_list, values, c="#15328e")

#hranice castecne - plne periodicke
alpha_list, values = findTresholdValues(data, numpy.arange(-4, 3.75, 0.125), ruleFullyPeriodic)
matplotlib.pyplot.scatter(alpha_list, values, marker="x", c="#8e3515", label="Plne periodicke (E[A] > 0.9)")
matplotlib.pyplot.plot(alpha_list, values, c="#8e3515")

#hranice periodicke - konstantni 1 / -1
alpha_list, values = findTresholdValues(data, numpy.arange(-4, 3.75, 0.125), ruleConstant)
matplotlib.pyplot.scatter(alpha_list, values, marker="x", c="#71158e", label="Konec periodicnosti (E > 0.9)")
matplotlib.pyplot.plot(alpha_list, values, c="#71158e")

#hranice nevlny - vlny
alpha_list, values = findTresholdValues(data, numpy.arange(-4, 3.75, 0.125), ruleWaves)
matplotlib.pyplot.scatter(alpha_list, values, marker="x", c="#11758e", label="Vznik vln")
matplotlib.pyplot.plot(alpha_list, values, c="#11758e")

ax.legend()
matplotlib.pyplot.grid(True)
matplotlib.pyplot.show()
fig.savefig("./diagram.jpg")
fig.savefig("./poznamky/phase_diagram.jpg")
