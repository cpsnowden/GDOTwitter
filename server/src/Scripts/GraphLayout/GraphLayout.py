import matplotlib.pyplot as plt
import csv
import numpy as np

def get_date(path):
    traction = []
    swing = []
    with open(path) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            i +=1
            if i == 1:
                continue
            if i == 1000:
                break
            traction.append(float(row[0]))
            swing.append(float(row[1]))
    plt.subplot(211)
    plt.plot(swing, label = "swing:" + path)
    plt.plot(traction, label = "tract:" + path)
    plt.subplot(212)
    plt.plot(np.array(swing) / np.array(traction), label = path)

    return traction, swing


get_date("Output/COG.dat")
get_date("Output/NoCOG.dat")
plt.legend()
plt.subplot(211)
plt.legend()
plt.show()
#
