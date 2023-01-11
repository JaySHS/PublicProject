#writer : Jay Shin
#created : Jan 11 2023

import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import pandas as pd
from IPython.display import display

#First : open file(csv)
filetype = (('csv files', '*.csv'), ('All files', '*.*'))
fn = filedialog.askopenfilename(filetypes=filetype)

file = open(fn, "r")
#Second : read data
name = file.readline().split(",")
name[-1] = name[-1].strip()

N = len(name)
temp = []
fname = []

for i in range(N):
    temp.append(name[i].replace("_", " "))
    fname.append(temp[i].replace("\"", ""))

data = []

for line in file:
    ldata = line.split(',')
    ldata[-1] = ldata[-1].strip()
    for i in range(len(ldata)):
        try:
            ldata[i] = float(ldata[i])
        except:
            ldata[i] = str(ldata[i])
    data.append(ldata)

print(type(data[10][10]))

arrdata = np.transpose(np.array(data))

dataset = {}
for i in range(N):
    dataset.update({fname[i] : arrdata[i]})
    
data_pd = pd.DataFrame(dataset)

ct = data_pd["critical temp"].to_numpy()
print(ct)
print(type(ct[0]))
#Third : create a dropdown menu
#Fourth : plot with the chosen axis