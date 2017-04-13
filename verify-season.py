import numpy as np
import os

data_path = "./seasons/2004/"
files = os.listdir(data_path)

count = 0
num_games = 0
for f in files:
    d = np.genfromtxt(data_path+f, delimiter=",")
    num_games = num_games + d.shape[0]
    count = count + 1

print float(num_games) / float(count)
