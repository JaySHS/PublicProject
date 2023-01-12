#writer : Jay Shin
#created : Jan 11 2023

import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import pandas as pd
from IPython.display import display

#Create a window with tkinter

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphical csv reader")
        self.geometry("1080x720")
        self.filetype = (('csv files', '*.csv'), ('All files', '*.*'))

    def run(self):
        self.btn_openfile = Button(text="open file", command=self.openfile)
        self.ent_filename = Entry(state=DISABLED, width=48)
        self.ent_filename.place(x=10, y=12)
        self.btn_openfile.place(x=310, y=10)
        self.mainloop()

    #Open file(csv)    
    def openfile(self):
        fn = filedialog.askopenfilename(filetypes=self.filetype)

        try:
            file = open(fn, "r")
            self.ent_filename.config(state=NORMAL)
            self.ent_filename.delete(0, END)
            self.ent_filename.insert(0, fn)
            self.ent_filename.config(state=DISABLED)
            readdata(file)
        except:
            print("Error : could not open file.")   
    
#Read data
def readdata(file):
    name = file.readline().split(",")
    name[-1] = name[-1].strip()

    N = len(name)
    temp = []
    fname = []

    for i in range(N):
        temp.append(name[i].replace("_", " "))
        fname.append(temp[i].replace("\"", ""))

    data = []

    iferror = False

    for line in file:
        ldata = line.split(',')
        ldata[-1] = ldata[-1].strip()
        for i in range(len(ldata)):
            try:
                ldata[i] = float(ldata[i])
            except:
                ldata[i] = 0
                iferror = True
        data.append(ldata)

    if(iferror):
        print("Error : Non-numeric data was found. It was replaced to 0.")

    arrdata = np.transpose(np.array(data, dtype=float))

    dataset = {}
    for i in range(N):
        dataset.update({fname[i] : arrdata[i]})
    
    data_pd = pd.DataFrame(dataset)

    return data_pd, fname

#Create a dropdown menu
win = App()
win.run()
#Plot with the chosen axis