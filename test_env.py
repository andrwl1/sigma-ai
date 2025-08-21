import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Numpy:", np.__version__)
print("Pandas:", pd.__version__)

import matplotlib
print("Matplotlib:", matplotlib.__version__)


x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title("Test Plot")
plt.show()
