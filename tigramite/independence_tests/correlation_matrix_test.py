from scipy import stats
import numpy as np
import sys
from independence_tests_base import CondIndTest
import time
import torch
import pandas as pd
import seaborn as sns
from pytorch_aux import *
import matplotlib.pyplot as plt

measure_lst = []

for size in [5000, 10000]:
    for _ in range(5):
        size = int(size)
        data_numpy = np.random.normal(size=(size, size))
        ts = time.time()
        np.corrcoef(data_numpy)
        numpy_time = time.time() - ts
        measure = {"Size": size, "Time": numpy_time,
                   "Library": "NumPy"}
        measure_lst.append(measure)

        data_torch = torch.randn((size, size))
        ts = time.time()
        corrcoef(data_torch)
        torch_time = time.time() - ts
        measure = {"Size": size, "Time": torch_time,
                   "Library": "TorchPy"}
        measure_lst.append(measure)

df = pd.DataFrame(measure_lst)

sns.lineplot(x="Size", y="Time", hue="Library", data=df)
plt.show()
