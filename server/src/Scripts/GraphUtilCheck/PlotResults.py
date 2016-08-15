import matplotlib.pyplot as plt
import numpy as np
import json

new = []
old = []
new_x = []
old_x = []
with open("test_results_2.dat") as f:
    for l in f:
        entry = json.loads(l)
        o = entry["oldT"]
        n = entry["newT"]
        print o,n
        if len(o) > 0:
            old.append(o)
            old_x.append(entry["nodes"])
        if len(n) > 0:
            new.append(n)
            new_x.append(entry["nodes"])

# old = np.array(old)
old_mean = np.array([np.array(i).mean() for i in old])
old_stdev = np.array([np.array(i).std() for i in old])
old_lens = np.array([np.sqrt(len(i)) for i in old])
old_sterr = old_stdev / old_lens

new_mean = np.array([np.array(i).mean() for i in new])
new_stdev = np.array([np.array(i).std() for i in new])
new_lens = np.array([np.sqrt(len(i)) for i in new])
new_sterr = new_stdev / new_lens

print new_lens

fig, axs = plt.subplots(nrows=1, ncols=2)
print axs
ax = axs[0]
l1 = ax.errorbar(old_x, old_mean, yerr=old_sterr, fmt='-o', label="Old Implementation")
l2 = ax.errorbar(new_x, new_mean, yerr=new_sterr, fmt='-o', label="New Implementation")
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'$N_{nodes}$', fontsize=15)
ax.set_ylabel("Time to fix .graphml file /s", fontsize=15)
plt.figlegend( (l1,l2), ("Old Implementation","New Implementation"), loc = 'upper center', ncol=5, labelspacing=0. )
ax = axs[1]
ax.errorbar(old_x, old_mean, yerr=old_sterr, fmt='-o')
ax.errorbar(new_x, new_mean, yerr=new_sterr, fmt='-o')
ax.set_xscale('log')
ax.set_xlabel(r'$N_{nodes}$', fontsize=15)
ax.set_ylabel("Time to fix .graphml file /s", fontsize=15)
# ax.set_title('Vert. symmetric')
plt.show()