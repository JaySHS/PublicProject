#writer : Jay Shin
#created : Jan 11 2023

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import pandas as pd
from pandastable import Table

#Create a window with tkinter

class App(Tk):
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("Graphical csv reader")
        master.geometry("1080x720")
        master.resizable(0,0)
        self.filetype = (('csv files', '*.csv'), ('All files', '*.*'))
        self.options = ["N/A"]
        self.xoptions = ["N/A"]
        self.plotoptions = ["N/A"]
        self.fileopened=False
        self.fn=''

        self.cmb_index_plot = StringVar()
        self.cmb_index_plot.set(self.plotoptions[0])
        self.cmb_index_x = StringVar()
        self.cmb_index_x.set(self.xoptions[0])
        self.cmb_index_y = StringVar()
        self.cmb_index_y.set(self.options[0])

    def run(self):
        self.withdraw()
        self.btn_openfile = Button(self.master, text="Open File", command=self.openfile)
        self.btn_draw = Button(self.master, text="Draw Graph", command=self.draw, width=18)
        self.btn_dataframe = Button(self.master, text="Show Dataframe", command=self.dataframe_window, width=18)
        self.btn_exit = Button(self.master, text="Exit", command=self.exitrun, width=18)
        self.ent_filename = Entry(self.master, state=DISABLED, width=48)
        self.ent_status = Entry(self.master, state=DISABLED, width=60)
        self.cmb_plot = Combobox(self.master, width=30, textvariable=self.cmb_index_plot, values=self.plotoptions, state='readonly')
        self.cmb_x = Combobox(self.master, width=30, textvariable=self.cmb_index_x, values=self.xoptions, state='readonly')
        self.cmb_y = Combobox(self.master, width=30, textvariable=self.cmb_index_y, values=self.options, state='readonly')
        
        self.btn_openfile.place(x=310, y=10)
        self.btn_draw.place(x=885, y=120)
        self.btn_dataframe.place(x=885, y=640)
        self.btn_exit.place(x=885, y=680)
        self.ent_filename.place(x=10, y=12)
        self.ent_status.place(x=400, y=12)
        self.cmb_plot.place(x=840, y=10)
        self.cmb_x.place(x=840, y=50)
        self.cmb_y.place(x=840, y=85)

        self.editentry(self.ent_status, "Waiting to open file...")

        self.master.mainloop()

    #Open file(csv)    
    def openfile(self):
        tempfn = filedialog.askopenfilename(filetypes=self.filetype)
        if(tempfn!=''):
            self.fn = tempfn

        try:
            file = open(self.fn, "r")
            self.fileopened=True
        except:
            if(self.fn==""):
                messagebox.showerror("Error", "Error : No file selected.")
                self.editentry(self.ent_status, "Error : No file selected.")
            else:
                messagebox.showerror("Error", "Error : Could not open file.")
                self.editentry(self.ent_status, "Error : Could not open file.")
        
        if(self.fileopened):
            self.editentry(self.ent_filename, self.fn)
            try:   
                self.dataframe, self.key, self.skey, self.xkey = readdata(file)
                self.options = self.key
                self.xoptions = self.xkey
                if(self.xkey!=[]):
                    self.plotoptions = plot_list['plottable']
                elif(self.key==[]):
                    self.plotoptions = plot_list['illegal']
                else:
                    self.plotoptions = plot_list['not_plottable']
                self.updatecmb(self.cmb_x, self.cmb_index_x, ["N/A"])
                self.updatecmb(self.cmb_y, self.cmb_index_y, ["N/A"])
                self.updatecmb(self.cmb_plot, self.cmb_index_plot, self.plotoptions)
                self.cmb_plot.bind('<<ComboboxSelected>>', self.configcmb)
                self.editentry(self.ent_status, "File loaded. Choose plot type.")
            except:
                messagebox.showerror("Error", "Error : Could not read data.")
                self.editentry(self.ent_status, "Error : Could not read data.")
            
    def editentry(self, entry, text):
        entry.config(state=NORMAL)
        entry.delete(0, END)
        entry.insert(0, text)
        entry.config(state=DISABLED)

    def configcmb(self, event):
        if(self.cmb_plot.get()=="Plot"):
            self.updatecmb(self.cmb_x, self.cmb_index_x, self.xoptions)
            self.updatecmb(self.cmb_y, self.cmb_index_y, self.options)
        elif(self.cmb_plot.get()=="Scatter"):
            self.updatecmb(self.cmb_x, self.cmb_index_x, self.options)
            self.updatecmb(self.cmb_y, self.cmb_index_y, self.options)
        elif(self.cmb_plot.get()=="Histogram"):
            self.updatecmb(self.cmb_x, self.cmb_index_x, self.options)
            self.updatecmb(self.cmb_y, self.cmb_index_y, ["N/A"])
        else:
            self.updatecmb(self.cmb_x, self.cmb_index_x, ["N/A"])
            self.updatecmb(self.cmb_y, self.cmb_index_y, ["N/A"])
        

    def updatecmb(self, cmb, cmb_index, options):
        cmb.config(values=options)
        cmb_index.set(options[0])

    def draw(self):
        if(self.fileopened):
            try:
                fig = plt.figure(figsize=(5,4), dpi=160)
                ax = fig.add_subplot()
                df_sort = self.dataframe.sort_values(by=self.cmb_x.get())
                if(self.cmb_plot.get()!="Histogram"):
                    plt.cla()
                    df_sort.plot(x=self.cmb_x.get(),  y=self.cmb_y.get(), 
                        kind=plot_type[self.cmb_plot.get()], ax=ax)
                else:
                    plt.cla()
                    df_sort.hist(column=self.cmb_x.get(), grid=False, ax=ax)

                plt.tight_layout()

                canvas = FigureCanvasTkAgg(fig, master=self.master)
                canvas.draw()
                canvas.get_tk_widget().place(x=10, y=70)
                self.editentry(self.ent_status, "Graphing completed.")
            except:
                if(self.cmb_plot.get()=="select plot type"):
                    messagebox.showerror("Error", "Error : Please select plot type.")
                    self.editentry(self.ent_status, "Error : Please select plot type.")
                else:
                    messagebox.showerror("Error", "Error : Could not graph data.")
                    self.editentry(self.ent_status, "Error : Could not graph data.")
        else:
            messagebox.showerror("Error", "Error : No file loaded.")
            self.editentry(self.ent_status, "Error : No file loaded.")

    def exitrun(self):
        plt.close('all')
        self.destroy()
        self.master.destroy()
    
    def dataframe_window(self):
        frame = Toplevel(self.master)
        self.table = Table(frame, dataframe=self.dataframe, showtoolbar=True, showstatusbar=True)
        self.table.show()



plot_list = {'plottable' :["select plot type", "Plot", "Scatter", "Histogram"],
    'not_plottable' : ["select plot type", "Scatter", "Histogram"],
    'illegal' : ["No option available"]
  }

plot_type = {'Plot' : 'line',
    'Scatter' : 'scatter'
}

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

    for line in file:
        ldata = line.split(',')
        ldata[-1] = ldata[-1].strip()
        data.append(ldata)

    arrdata = np.transpose(np.array(data, dtype=object))

    dataset = {}
    for i in range(N):
        dataset.update({fname[i] : arrdata[i]})
    
    data_pd = pd.DataFrame(dataset)

    numcolumn = []
    plottablex = []
    stringcolumn = []
    index = 0

    for column in data_pd:
        try:
            data_pd[column] = data_pd[column].astype(float)
            numcolumn.append(fname[index])
            if(data_pd[column].is_unique):
                plottablex.append(fname[index])
        except:
            stringcolumn.append(fname[index])
        index += 1

    return data_pd, numcolumn, stringcolumn, plottablex

root = Tk()
win = App(root)
win.run()