#!/usr/bin/env python

import matplotlib.pyplot as plt

# year = [1960, 1970, 1980, 1990, 2000, 2010]
# pop_pakistan = [44.91, 58.09, 78.07, 107.7, 138.5, 170.6]
# pop_india = [449.48, 553.57, 696.783, 870.133, 1000.4, 1309.1]
# plt.plot(year, pop_pakistan, color='g')
# plt.plot(year, pop_india, color='orange')
# plt.xlabel('Countries')
# plt.ylabel('Population in million')
# plt.title('Pakistan India Population till 2010')
# plt.show()

# 10000,1,655
# 10000,2,738
# 20000,1,403
# 20000,2,401

x = [1, 2]
y = [655, 738]
z = [403, 401]

plt.plot(x, y, 'o-')
for a,b in zip(x, y): 
    plt.text(a, b, ' ' + str(b), size='15')

plt.plot(x, z, 'o-')
for a,b in zip(x, z): 
    plt.text(a, b, ' ' + str(b), size='15')

plt.show()

# https://matplotlib.org/gallery/text_labels_and_annotations/arrow_demo.html#sphx-glr-gallery-text-labels-and-annotations-arrow-demo-py
# https://scitools.org.uk/iris/docs/v1.9.0/html/userguide/plotting_a_cube.html
# https://matplotlib.org/gallery/misc/coords_report.html#sphx-glr-gallery-misc-coords-report-py
# https://stackoverflow.com/questions/6282058/writing-numerical-values-on-the-plot-with-matplotlib
