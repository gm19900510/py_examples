# -*- coding: utf-8 -*-
import numpy as np

v = np.array([9, 10])

index = np.argwhere(v == 8)
print(len(index))