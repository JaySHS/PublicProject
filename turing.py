import numpy as np
from tkinter import *
from tkinter.ttk import *

dir = {
    "L": [0, 0],
    "S": [0, 1],
    "R": [1, 0]
}

def UPP(txt):
    utxt = ""
    for i in range(len(txt)):
        if ord(txt[i]) >= 97 and ord(txt[i]) <= 122:
            utxt += (chr(ord(txt[i])-32))
        else:
            utxt += (txt[i])
    return utxt

def APP(list, p):
    list = np.append(list, 0)
    for i in reversed(range(len(list))):
        list[i] = list[i-1].copy()
    list[0] = 0
    p += 1
    return list, p

def BTD(bin):
    dec = 0
    b = len(bin)
    for i in range(b):
        dec += bin[i]*2**(b-i-1)
    return dec

def DTBn(dec, n):
    if n == 0:
        while(dec//(2**n) >= 1):
            n += 1
    bin = np.zeros((n))
    for i in reversed(range(n)):
        if dec >= 2**i:
            bin[n-1-i] = 1
            dec -= 2**i
    return bin

def NCODE(ns):
    narr = np.zeros([5])
    if ns == "0":
        narr = [1, 1, 1, 1, 1]
    elif ord(ns) >= 65 and ord(ns) <= 90:
        narr = DTBn(ord(ns)-ord("A"), 5)
    elif ord(ns) >= 97 and ord(ns) <= 122:
        narr = DTBn(ord(ns)-ord("a"), 5)
    else:
        narr = [1, 1, 0, 1, 1]
    return narr

def ACT(code):
    decarray = np.array([int(code[0])])
    decarray = np.append(decarray, dir[code[1]])
    decarray = np.append(decarray, NCODE(code[2]))
    decarray = np.append(decarray, int(code[3]))
    decarray = np.append(decarray, dir[code[4]])
    decarray = np.append(decarray, NCODE(code[5]))
    return decarray

class STATE:
    def __init__(self, list, p):
        self.list = list
        self.p = p
        self.con = np.zeros((2,3))
        self.curcon = np.zeros(3)

    def setstate(self, v, chg, mov, nextstate):
        self.con[v][0] = chg
        self.con[v][1] = mov
        self.con[v][2] = nextstate

    def RED(self):
        if self.list[self.p] == 1:
            self.curcon[:] = self.con[1][:]
        else:
            self.curcon[:] = self.con[0][:]

    def WRI(self):
        self.list[self.p] = self.curcon[0]

    def MOV(self):
        if self.curcon[1] == 0:
            self.p -= 1
        elif self.curcon[1] == 2:
            self.p += 1
    
    def EXE(self):
        self.RED()
        self.WRI()
        self.MOV()
        return self.list, self.p, self.curcon[2]

class PROG:
    def __init__(self, list):
        self.curstate = 0
        self.slist = np.zeros((31,6))
        self.csdata = np.zeros((6))
        self.scount = 0
        self.list = list.copy()
        self.listog = list
        self.p = 0
        self.step = 0
    
    def addstate(self, act):
        vcode = ACT(act)
        snum = self.scount
        v0 = np.zeros((3))
        v1 = np.zeros((3))

        v0[0] = BTD(vcode[0:1])
        v0[1] = BTD(vcode[1:3])
        v0[2] = BTD(vcode[3:8])
        v1[0] = BTD(vcode[8:9])
        v1[1] = BTD(vcode[9:11])
        v1[2] = BTD(vcode[11:16])

        self.slist[snum][0] = v0[0]
        self.slist[snum][1] = v0[1]
        self.slist[snum][2] = v0[2]
        self.slist[snum][3] = v1[0]
        self.slist[snum][4] = v1[1]
        self.slist[snum][5] = v1[2]
        self.scount += 1

    def readstate(self):
        self.csdata = self.slist[int(self.curstate)][:]
    
    def exestate(self):
        self.readstate()
        s = STATE(self.list, self.p)
        s.setstate(0, self.csdata[0], self.csdata[1], self.csdata[2])
        s.setstate(1, self.csdata[3], self.csdata[4], self.csdata[5])
        self.list, self.p, self.curstate = s.EXE()
        if self.p < 0:
            self.list, self.p = APP(self.list, self.p)
        elif self.p >= len(self.list):
            self.list = np.append(self.list, 0)
        self.step += 1
        print("step", self.step, ":", self.list, "/ p = ", self.p, "/ state = ", int(self.curstate))
    
    def checkterm(self):
        if self.curstate == 31:
            return 0
        else:
            return 1
    
    def RUN(self):
        if self.scount != 0:
            print("step 0 :", self.list, "/ p = ", self.p, "/ state = ", int(self.curstate))
            while(self.checkterm()):
                self.exestate()
        else:
            print("Illegal Condition : no state found")

            # BB count
            # count = 0
            # for i in range(len(self.list)):
            #     count += self.list[i]
        print("HALT!")

statenum = 0

def addstate():
    txt = UPP(ent.get())
    p.addstate(txt)
    lbl_state["text"] = lbl_state["text"] + "\nState " + chr(p.scount+64) + " : " + txt
    ent.delete(0, END)

def run():
    win.destroy()

tape = np.zeros((1))
p = PROG(tape)

win = Tk()
win.geometry("300x200")
win.title("Action Table Input")
ent = Entry()
lbl_state = Label(text="Action Table")
btn_add = Button(text = "Add", command=addstate)
btn_run = Button(text = "Run", command=run)

ent.pack(padx=5, pady=10,)
btn_add.pack()
lbl_state.pack()
btn_run.pack()

win.mainloop()

# p.addstate("1RB1LB")
# p.addstate("1LA0LC")
# p.addstate("1R01LD")
# p.addstate("1RD0RA")

p.RUN()