"""
solves differential equations of the form: n = -a (dn/dx)
"""
import matplotlib.pyplot as plotto
import numpy as np
from matplotlib.widgets import TextBox


def default():
    return 0.0, 10.0, .1, 2, 2, 3


def start_up():
    start = float(input("start at x=?"))
    stop = float(input("stop at x=?"))
    dx = float(input("step=?"))
    a = float(input("a=?"))
    x = float(input("x coordinate of known point?"))
    n = float(input("n(x)=?"))
    return start, stop, dx, a, x, n


def solver(start, stop, step, a, n_known, x_known):
    k = (a / step - .5) / (a / step + .5)

    if start > stop:  # flippy flippy
        temp = stop
        stop = start
        start = temp
        temp = None
    if x_known > stop: #take care of out of bounds
        stop = x_known
    if x_known < start:
        start = x_known
    print(start,x_known,stop)
    x_index = int((x_known - start) / step)  # x goes from coord to index

    number = int((stop - start) / step)+1
    values = [0.0] * number  # kinda instantiating the list
    print(x_index, number)
    values[x_index] = n_known
    if x_known >= 0:  # does the math step by step
        for i in range(0, x_index):  # counts down from known value
            values[x_index - 1 - i] = values[x_index - i] / k
        if x_known < number:  # makes sure x+1 is <= number
            for i in range(x_index + 1, number): # counts up from known value
                values[i] = values[i - 1] * k
    list_x=[]
    for i in range(0,number): # gets the x coordinates
        list_x.append(start+step*i)
    plotto.plot(list_x, values)
    plotto.xlabel("x")
    plotto.ylabel("y")


def solver_matrix(start, stop, step, a, n_known, x_known):
    if start > stop:  # flippy flippy if need
        temp = stop
        stop = start
        start = temp
    number = int((stop - start) / step)  # number of iterations / rows/ columns
    x_index = int((x_known - start) / step)


    k1 = (-a/step-1/2)
    k2 = (a/step-1/2)
    to_be_matrix = []
    for i in range(0,number):
        to_be_matrix.append([0.0]*number)
        if i>=1:
            to_be_matrix[i][i] = k1
            to_be_matrix[i][i-1] = k2
    to_be_matrix[0][x_index]=1
    mat=np.matrix(to_be_matrix)
    to_be_matrix2 = []

    for i in range(0,number):
        to_be_matrix2.append(0)
    to_be_matrix2[0] = n_known
    list_x = []
    for i in range(0,number):  # gets the x coordinates
        list_x.append(start+step*i)

    answer_mat = np.matrix(to_be_matrix2).getT()
    return list_x, np.matmul(mat.getI(), answer_mat)


start, stop, dx, a, x, n = default()
xdata, ydata=solver_matrix(start, stop, dx, a, n, x)

fig, ax = plotto.subplots()
l, = plotto.plot(xdata, ydata)
plotto.subplots_adjust(bottom=.5)


def submit_a(text):
    global start, stop, dx, a, n, x, l
    a = float(text)
    x_list, y_list = solver_matrix(start, stop, dx, a, n, x)
    #plotto.axes([np.min(x_list),np.max(x_list),np.min(y_list),np.max(y_list)])
    l.set_ydata(y_list)
    ax.set_ylim(np.min(y_list), np.max(y_list))
    plotto.draw()


a_text_box = TextBox(plotto.axes([0.6, 0.425, 0.3, 0.075]), 'a=', initial=a.__str__())
a_text_box.on_submit(submit_a)

def submit_start(text):
    global start, stop, dx, a, n, x, l
    start = float(text)
    x_list, y_list = solver_matrix(start, stop, dx, a, n, x)
    plotto.set_xlim(xmin=start)
    l.set_ydata(y_list)
    ax.set_ylim(np.min(y_list), np.max(y_list))
    #plotto.draw()


start_text_box = TextBox(plotto.axes([0.1, 0.05, 0.3, 0.075]), 'start at', initial=start.__str__())
start_text_box.on_submit(submit_start)


plotto.show()

