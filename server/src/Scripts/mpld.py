# import matplotlib.pyplot as plt, mpld3
#
#
#
# dpi = 10
# fig, ax = plt.subplots(figsize=(1920/dpi, 1080/dpi), dpi=dpi, subplot_kw=dict(axisbg='#EEEEEE'))
# scatter = ax.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
#
#
# tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=["one","two","three","four","five"])
# mpld3.plugins.connect(fig, tooltip)
#
# g = mpld3.fig_to_html(fig)
# # mpld3.show()
#
# mpld3.show()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins

# Define some CSS to control our custom labels
css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""

fig, ax = plt.subplots()
ax.grid(True, alpha=0.3)

N = 50
df = pd.DataFrame(index=range(N))
df['x'] = np.random.randn(N)
df['y'] = np.random.randn(N)
df['z'] = np.random.randn(N)

labels = []
for i in range(N):
    label = df.ix[[i], :].T
    label.columns = ['Row {0}'.format(i)]
    # .to_html() is unicode; so make leading 'u' go away with str()
    labels.append(str(label.to_html()))

points = ax.plot(df.x, df.y, 'o', color='b',
                 mec='k', ms=15, mew=1, alpha=.6)
print points
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('HTML tooltips', size=20)

# tooltip = plugins.PointHTMLTooltip(points[0], labels,
#                                    voffset=10, hoffset=10, css=css)
tooltip = mpld3.plugins.PointLabelTooltip(points[0])
plugins.connect(fig, plugins.Reset(), plugins.BoxZoom(), plugins.Zoom())
plugins.connect(fig, tooltip)


g = mpld3.fig_to_html(fig)
with open("out.html","w") as f:
    f.write(g)

# plt.close('all')
#
mpld3.show()


import matplotlib.pyplot as plt
import numpy as np
import mpld3

fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
N = 100

scatter = ax.scatter(np.random.normal(size=N),
                     np.random.normal(size=N),
                     c=np.random.random(size=N),
                     s=1000 * np.random.random(size=N),
                     alpha=0.3,
                     cmap=plt.cm.jet)
ax.grid(color='white', linestyle='solid')

ax.set_title("Scatter Plot (with tooltips!)", size=20)

labels = ['point {0}'.format(i + 1) for i in range(N)]
print labels
tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
mpld3.plugins.connect(fig, tooltip)

mpld3.show()