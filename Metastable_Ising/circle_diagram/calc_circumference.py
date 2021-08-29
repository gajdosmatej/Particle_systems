import numpy
import math

def calcCircumference():
    f = open("average.txt", "r")
    line = f.readline()
    line_num = 0
    circumference = 0
    prev_X, prev_Y = None,None
    itr = 1

    while line != "":
        line_num += 1
        if line_num > itr*250:
            print("Parsed " + str(itr*250) + " lines")
            itr += 1

        break_index = line.index(" ")
        #time = line[:break_index]
        vals = line[break_index+1:]
        break_index = vals.index(" ")
        X = float(vals[:break_index])
        Y = float(vals[break_index:])
        if prev_X != None:
            circumference += math.sqrt( pow(X - prev_X, 2) + pow(Y - prev_Y, 2) )
        prev_X = X
        prev_Y = Y

        line = f.readline()

    print("o = " + str(circumference))
    return circumference
