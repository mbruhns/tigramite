import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 100, 10)
y = x ** 2

plt.scatter(x,y, marker='X', facecolor='r', edgecolor='k', s=100)
plt.show()