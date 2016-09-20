import matplotlib.pyplot as plt
import json

import numpy as np

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

ranges = [1,3,5,7]

colors = ["b","r","g","k"]

for j,i in enumerate(ranges):
    # data = json.load(open("THREADING/TEST_" + str(i) + "_toolkit.dat"))
    # d = moving_average(data[:1000],5)
    # plt.plot(d/10e6, linestyle='-', color = colors[j])
    # # , color = tableau20[j])


    data = json.load(open("THREADING/TEST_10000_toolkit_" + str(i) + ".dat"))
    d = moving_average(data[:1000], 5)
    plt.plot(d / 10e6, linestyle="-", color = colors[j])

    data = json.load(open("THREADING/TEST_10000_native_" + str(i) + ".dat"))
    d = moving_average(data[:1000], 5)
    plt.plot(d / 10e6, linestyle="-.", color=colors[j])

    # , color = tableau20[j])

plt.show()