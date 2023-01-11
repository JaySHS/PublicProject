import numpy as np
from tkinter import *
from tkinter.ttk import *

def comparetext(text, letter):
    for i in range(len(text)):
        if text[i] == letter:
            return 1
    return 0

class App(Tk):

    opdic = {
        "+": 1,
        "-": 2,
        "*": 3,
        "/": 4
    }

    def __init__(self):
        super().__init__()
        self.npbtnarray = []
        self.opbtnarray = []
        self.lbl_eq = Label(text = "")
        self.lbl_res = Label(text = "", anchor="e")
        self.ent = Entry()
        self.state = 0
        self.num1 = 0
        self.num2 = 0
        self.geometry("350x200")
        self.title("Calculator")

    def binput(self, txt):
        if self.ent.get() == "0":
            self.ent.delete(0, END)
        elif self.ent.get() == "-0":
            self.ent.delete(0, END)
            self.ent.insert(0, "-")
        self.ent.insert(END, txt)
    
    def addpoint(self):
        if self.ent.get() == "":
            self.ent.insert(END, "0")
        if not comparetext(self.ent.get(), "."):
            self.ent.insert(END, ".")

    def changesign(self):
        if self.ent.get() == "":
            self.ent.insert(END, "-0")
        else:
            if self.ent.get()[0] == "-":
                self.ent.delete(0)
            else:
                self.ent.insert(0, "-")
    
    def op(self, txt):
        number = self.ent.get()
        if self.state() == 0:
            if number == "" or number == "-0":
                number = "0"
            self.num1 = float(number)
            self.lbl_eq["text"] += number + txt
            self.ent.delete(0, END)
            self.state = self.opdic[txt]
        else:
            if number == "":
                number = str(self.num1)
            self.num2 = float(number)
    
    def eq(self):
        if self.state == 0:
            number = self.ent.get()
            if (number == "" and self.lbl_res["text"] == "") or number == "-0":
                number = "0"
            elif number == "" and self.lbl_res["text"] != "":
                number = self.lbl_res["text"]
            self.lbl_eq["text"] = number + "="
            self.lbl_res["text"] = number
        self.ent.delete(0, END)
        self.state = 0

    
    def addleftbutton(self, txt):
        self.npbtnarray.append(Button(text = txt, command=lambda: self.binput(txt)))
    
    def addsignbutton(self):
        self.npbtnarray.append(Button(text = "+/-", command=self.changesign))
    
    def addpointbutton(self):
        self.npbtnarray.append(Button(text = ".", command=self.addpoint))

    def addeqbutton(self):
        self.opbtnarray.append(Button(text = "=", command=self.eq))
    
    def addplusbutton(self):
        self.opbtnarray.append(Button(text = "+", command=lambda: self.op("+")))

    def numpad(self):
        self.addleftbutton("1")
        self.addleftbutton("2")
        self.addleftbutton("3")
        self.addleftbutton("4")
        self.addleftbutton("5")
        self.addleftbutton("6")
        self.addleftbutton("7")
        self.addleftbutton("8")
        self.addleftbutton("9")
        self.addsignbutton()
        self.addleftbutton("0")
        self.addpointbutton()

    def operator(self):
        self.addeqbutton()
        self.addplusbutton()

    def RUN(self):
        self.numpad()
        self.operator()
        self.lbl_eq.grid(row = 0, column = 0, columnspan = 4, sticky="nsew")
        self.lbl_res.grid(row = 1, column = 0, columnspan = 4, sticky="nsew")
        self.ent.grid(row = 2, column = 0, columnspan = 4, sticky="nsew")
        for i in range(len(self.npbtnarray)):
            self.npbtnarray[i].grid(row = i//3+3, column = i%3)
        for i in range(len(self.opbtnarray)):
            self.opbtnarray[i].grid(row = i+3, column = 3, padx = 10)
        self.mainloop()


win = App()
win.RUN()