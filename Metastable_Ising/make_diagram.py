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
    return numpy.array(alpha_list), numpy.array(treshold_values)


def ruleConstant(data_list):
    return ( numpy.logical_and(abs(data_list[:,2]) > 0.5, data_list[:,4] > 0.8) )

def rulePartiallyPeriodic(data_list):
    return ( numpy.logical_and(data_list[:,4] > 0.3, data_list[:,2] < 0.5) )   #abs neni, protoze v datech jsou amplitudy maxim

def ruleFullyPeriodic(data_list):
    return ( numpy.logical_and(data_list[:,4] > 0.9, data_list[:,2] < 0.5 ) )

def ruleWaves(data_list):
    return (data_list[:,7] < 0.12)


f = open("./expected_values.txt", "r")
f.readline()    #1. radek

fig, ax = matplotlib.pyplot.subplots()

ax.set_xlabel(r"$\alpha$",fontsize=12)
ax.set_ylabel(r"$\beta$", fontsize=12)
ax.set_title("Fazovy diagram - Metastable Ising Model")
ax.set_xlim([0,3.5])
ax.set_ylim([1,13])


data = numpy.array([])

data_line = parseLine()
while data_line != None:
    data = numpy.append(data, data_line)
    #matplotlib.pyplot.scatter(data_line[0], data_line[1],c="red")
    data_line = parseLine()

data = numpy.reshape(data, (-1,8))  #radek ma 8 polozek
data = data[data[:,0] >= 0]

alpha_points = numpy.arange(0, 3.75, 0.005)
#hranice nahodne - periodicke
alpha_list, values = findTresholdValues(data, alpha_points, rulePartiallyPeriodic)
matplotlib.pyplot.scatter(alpha_list, values, marker="|", c="#15328e", label="Zacatek periodicnosti (E[A] > 0.3)")
matplotlib.pyplot.plot(alpha_list, values, c="#15328e")

#hranice castecne - plne periodicke
alpha_list_upper, values_upper = findTresholdValues(data, alpha_points, ruleFullyPeriodic)
matplotlib.pyplot.scatter(alpha_list_upper, values_upper, marker="|", c="#8e3515", label="Plne periodicke (E[A] > 0.9)")
matplotlib.pyplot.plot(alpha_list_upper, values_upper, c="#8e3515")

mask = numpy.isin(alpha_list, alpha_list_upper)
alpha_list = alpha_list[mask]
values = values[mask]

x = range(0,5)
y = range(2,6)
z = [[z] * 5 for z in range(4)]

num_bars = 100  # more bars = smoother gradient

#matplotlib.pyplot.contourf(x, y, z, num_bars, cmap=matplotlib.pyplot.cm.BuPu)
background_color = 'w'

y_max_curve = [ax.get_ylim()[1] for i in alpha_list]
#matplotlib.pyplot.fill_between(alpha_list, values, y2=0, color=background_color)
#matplotlib.pyplot.fill_between(alpha_list, values_upper, y2=y_max_curve, color=background_color)
#matplotlib.pyplot.fill_between(alpha_list, values, values_upper, color="blue")

alpha_list = alpha_list_upper
values = values_upper

#hranice periodicke - konstantni 1 / -1
alpha_list_upper, values_upper = findTresholdValues(data, alpha_points, ruleConstant)
matplotlib.pyplot.scatter(alpha_list_upper, values_upper, marker="|", c="#71158e", label="Konec periodicnosti (|E| > 0.9)")
matplotlib.pyplot.plot(alpha_list_upper, values_upper, c="#71158e")

mask = numpy.isin(alpha_list, alpha_list_upper)
alpha_list = alpha_list[mask]
values = values[mask]

y_max_curve = [ax.get_ylim()[1] for i in alpha_list_upper]
#matplotlib.pyplot.fill_between(alpha_list, values, y2=values_upper, color="purple")
#matplotlib.pyplot.fill_between(alpha_list_upper, values_upper, y2=y_max_curve, color="white")

#hranice nevlny - vlny
#alpha_list, values = findTresholdValues(data, numpy.arange(-4, 3.75, 0.125), ruleWaves)
#matplotlib.pyplot.scatter(alpha_list, values, marker="x", c="#11758e", label="Vznik vln")
#matplotlib.pyplot.plot(alpha_list, values, c="#11758e")

ax.legend()
matplotlib.pyplot.grid(True)
matplotlib.pyplot.show()
fig.savefig("./diagram.jpg")
fig.savefig("./poznamky/phase_diagram.jpg")
