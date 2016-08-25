import matplotlib.pyplot as plt
import json
import numpy as np
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

tableau20 = [(44, 160, 44),(214, 39, 40),(148, 103, 189),(199, 199, 199)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

data = json.load(open("TrumpClintonSaundersLouvian.json"))

for i in data:
    print i

fig,ax = plt.subplots()

x = np.arange(0,3)
width = 0.2


trump = data[0][1]
sanders = data[1][1]
clinton = data[2][1]

print trump



#
for i,j in enumerate(["Trump","Clinton","Saunders","Unclassified"]):
    rect = ax.bar(x  + i*width, [trump[j],clinton[j],sanders[j]], width, color = tableau20[i], alpha = 0.4, label=j)

ax.set_xticks(x + width*2)
ax.set_xticklabels(["Trump","Clinton","Sanders"])
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.spines["top"].set_visible(False)
plt.yticks(np.arange(0, 12000, 2000), [str(x/1000) for x in range(0, 12000, 2000)], fontsize=14)
for y in np.arange(0, 12000, 2000):
    plt.plot(range(0,4),[y] * len(range(0,4)),"--", lw=0.5, color = "black", alpha = 0.3)
ax.spines["right"].set_visible(False)
# fig,ax = plt.subplots()
# for i in xrange(len(tableau20)):
#     ax.bar(i * 10, 1, 10, color = tableau20[i])
plt.legend()
plt.xlabel("Louvian Community")
plt.ylabel("Number of Users in each Classification /thousand")
plt.show()