#writer : Jay Shin
#created : Jan 11 2023

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import pandas as pd

#Create a window with tkinter

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphical csv reader")
        self.geometry("1080x720")
        self.resizable(0,0)
        self.filetype = (('csv files', '*.csv'), ('All files', '*.*'))
        self.options = ["N/A"]

        self.drop_index_x = StringVar()
        self.drop_index_x.set(self.options[0])
        self.drop_index_y = StringVar()
        self.drop_index_y.set(self.options[0])

    def run(self):
        self.btn_openfile = Button(text="Open File", command=self.openfile)
        self.btn_draw = Button(text="Draw Graph", command=self.draw)
        self.btn_exit = Button(text="Exit", command=self.destroy)
        self.ent_filename = Entry(state=DISABLED, width=48)
        self.drop_x = OptionMenu(self, self.drop_index_x, *self.options)
        self.drop_y = OptionMenu(self, self.drop_index_y, *self.options)
        
        self.ent_filename.place(x=10, y=12)
        self.btn_openfile.place(x=310, y=10)
        self.btn_draw.place(x=880, y=100)
        self.btn_exit.place(x=920, y=680)
        self.drop_x.place(x=880, y=10)
        self.drop_y.place(x=880, y=45)

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
            self.dataframe, self.key = readdata(file)

            self.options = self.key
            self.updateDD(self.drop_x, self.drop_index_x, self.options)
            self.updateDD(self.drop_y, self.drop_index_y, self.options)
        except:
            print("Error : could not open file.")

    def updateDD(self, drop, drop_index, options):
        menu = drop["menu"]
        menu.delete(0, END)
        for string in options:
            menu.add_command(label=string, command=lambda value=string:drop_index.set(value))
        drop_index.set(options[0])

    def draw(self):
        fig = plt.figure(figsize=(5,4), dpi=160)
        ax = fig.add_subplot()

        self.dataframe.plot.scatter(x=self.drop_index_x.get(), y=self.drop_index_y.get(), ax=ax)
        ax.set_xlabel(self.drop_index_x.get())
        ax.set_ylabel(self.drop_index_y.get())

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=70)

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