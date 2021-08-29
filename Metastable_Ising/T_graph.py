import json
import numpy
import matplotlib
import matplotlib.pyplot

parse_num_text = 250


time_list = []
beta_list = []
step_list = []

f = open("./perioda.txt", "r")
line = f.readline()
line = f.readline()
line_num, iter = 0, 0

while line != "":
    line_num += 1
    if line_num > iter*parse_num_text:
        print("Parsed " + str(iter*parse_num_text) + " lines")
        iter += 1

    break_index = line.index(" ")

    beta_time_step = line[break_index+1:]
    break_index = beta_time_step.index(" ")
    beta = beta_time_step[:break_index]

    time_step = beta_time_step[break_index+1:]
    break_index = time_step.index(" ")
    time = time_step[:break_index]
    step = time_step[break_index+1:]
    if time != "nan":
        time_list.append(float(time))
        beta_list.append(float(beta))
        step_list.append(float(step))

    line = f.readline()

#print(time)
fig, ax = matplotlib.pyplot.subplots()
#ax.plot(beta_list, step_list)
ax.plot(beta_list, time_list, marker='o', linestyle='none', markersize=4, label = "Data")

#u = numpy.log(31227.43)
#v = numpy.log(39.71)
#a = numpy.exp(v*numpy.power(v/u, 2/3))
#b = numpy.power(u/v, 2/9)
fit_x = numpy.linspace(3, 7.7, 100)
#fit_y = 4*numpy.exp(numpy.power(1.324, fit_x))
#fit_y = numpy.power(a, numpy.power(b, fit_x))
fit_y = 4*numpy.exp(fit_x)/(7.8-fit_x)+27
ax.plot(fit_x, fit_y, linewidth=2, label = r'f$(x) = 4\exp{\frac{x}{7.8-x}} + 27$')
matplotlib.pyplot.legend()
ax.set(xlabel=r'$\beta$', ylabel='T',
       title=r'$T(\beta)$ proložené křivkou')

matplotlib.pyplot.yscale("log")
fig.savefig("./T_beta_img.jpg")
matplotlib.pyplot.show()
