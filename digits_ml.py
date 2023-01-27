import numpy as np
from sklearn.datasets import load_digits
import pandas as pd
from pandastable import Table
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
# import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import sys, os, subprocess

class Tkoutput():
    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll
    
    def write(self, text):
        self.widget.insert('end', text)
        if(self.autoscroll):
            self.widget.see("end")
    
    def flush(self):
        pass

class App(Tk):
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("digits_ml")
        self.stdout = sys.stdout
        self.df = load_digits(as_frame = True)

    def place(self):
        self.btn_plot = Button(text = "Plot", command=self.plot)
        self.btn_df = Button(text="Data", command=self.df_window)
        self.btn_exit = Button(text="Exit", command=self.terminate)
        self.ent = Entry()
        # self.txt = Text(state=DISABLED)
        # self.txt.pack()
        self.ent.pack()
        self.btn_plot.pack()
        self.btn_df.pack()
        self.btn_exit.pack()
    
    # def print(self, widget, text):
    #     self.txt.config(state=NORMAL)
    #     sys.stdout = Tkoutput(widget)
    #     print(text)
    #     sys.stdout = self.stdout
    #     self.txt.config(state=DISABLED)

    def plot(self):
        frame = Toplevel(self.master)
        fig = plt.figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot()

        datanum = int(self.ent.get())

        ax.matshow(self.df.images[datanum], cmap='gist_yarg')

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def df_window(self):
        frame = Toplevel(self.master)
        self.table = Table(frame, dataframe=self.df.data, showtoolbar=True, showstatusbar=True)
        self.table.show()

    def run(self):
        self.place()
        self.withdraw()
        # self.print(self.txt, "Hello, world!")
        self.master.mainloop()
    
    def terminate(self):
        plt.close('all')
        self.destroy()
        self.master.destroy()


root = Tk()
win = App(root)
win.run()