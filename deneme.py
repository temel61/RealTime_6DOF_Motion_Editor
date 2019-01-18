import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

x, y = np.mgrid[-2 : 2 : 20j, -2 : 2 : 20j]
z = 50 * np.sin(x + y)                     # test data
output = plt.subplot(111, projection = '3d')   # 3d projection
output.plot_surface(x, y, z, rstride = 2, cstride = 1, cmap = plt.cm.Blues_r)
output.set_xlabel('x')                         # axis label
output.set_xlabel('y')
output.set_xlabel('z')

plt.show()