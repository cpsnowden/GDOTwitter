import numpy as np

def step4(d):

    n = len(d)
    dbar = np.mean(d)
    dsbar = np.mean(np.multiply(d,d))
    fac = dsbar - np.square(dbar)
    summ = 0
    summup = []

    for z in range(n):
        summ += d[z]
        summup.append(summ)
    y = []
    for m in range(n-1):
        pos = m+1
        mscale = 4 * pos * (n - pos)
        Q = summup[m] - (summ - summup[m])
        U = -np.square(dbar * (n-2*pos) + Q) / float(mscale) + fac
        y.append(-(n/float(2) - 1)*np.log(n * U/2) - 0.5*np.log(pos * (n-pos)))

    z,zz = np.max(y), np.argmax(y)

    mean1 = sum(d[:zz+1])/float(len(d[:zz+1]))
    mean2 = sum(d[(zz+1):n])/float(n-1-zz)

    return y, zz, mean1, mean2
