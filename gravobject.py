import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from mpl_toolkits import mplot3d


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.magnitude = np.sqrt(x**2 + y**2 + z**2)
    
    def __str__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def unit(self):
        return Vector(self.x/self.magnitude, self.y/self.magnitude, self.z/self.magnitude)
    
    def smulti(self, k):
        return Vector(k*self.x, k*self.y, k*self.z)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __mul__(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

class Object:
    def __init__(self, r, v, m, t = 0):
        self.r = r
        self.v = v
        self.m = m
        self.t = t

    def gforce(self, other):
        dr = other.r - self.r
        dir = dr.unit()
        mag = G*self.m*other.m/(dr.magnitude)**2
        return dir.smulti(mag)

    def nextstate(self, a, dt):
        return Object(self.r+self.v.smulti(dt), self.v+a.smulti(dt), self.m, self.t+dt)
    
    def copy(self):
        return Object(self.r, self.v, self.m, self.t)

# G = 6.6743 * 10**(-11)
G = 1
dt = 0.001
ff = 100
tmax = 100
r1 = Vector(50, 0, 0)
v1 = Vector(-1, -1, -1)
o1 = Object(r1, v1, 400)

r2 = Vector(0, 10, 0)
v2 = Vector(-1, 1, 1)
o2 = Object(r2, v2, 30)

r3 = Vector(0, 0, 10)
v3 = Vector(1, 0, 1)
o3 = Object(r3, v3, 30)

fig = plt.figure()
ax = plt.axes(projection = "3d")

x1line = []
y1line = []
z1line = []

x2line = []
y2line = []
z2line = []

x3line = []
y3line = []
z3line = []

line1, = ax.plot([],[],[])
line2, = ax.plot([],[],[])
line3, = ax.plot([],[],[])

point1 = ax.scatter(0,0,0)
point2 = ax.scatter(0,0,0)
point3 = ax.scatter(0,0,0)

def movement(i):
    global o1, o2, o3

    for j in range(ff):
        x1 = o1.r.x
        y1 = o1.r.y
        z1 = o1.r.z

        x2 = o2.r.x
        y2 = o2.r.y
        z2 = o2.r.z

        x3 = o3.r.x
        y3 = o3.r.y
        z3 = o3.r.z

        x1line.append(x1)
        y1line.append(y1)
        z1line.append(z1)

        x2line.append(x2)
        y2line.append(y2)
        z2line.append(z2)

        x3line.append(x3)
        y3line.append(y3)
        z3line.append(z3)

        o1_next = o1.nextstate(o1.gforce(o2).smulti(1/o1.m) + o1.gforce(o3).smulti(1/o1.m), dt)
        o2_next = o2.nextstate(o2.gforce(o1).smulti(1/o2.m) + o2.gforce(o3).smulti(1/o2.m), dt)
        o3_next = o3.nextstate(o3.gforce(o1).smulti(1/o3.m) + o3.gforce(o2).smulti(1/o3.m), dt)

        o1 = o1_next.copy()
        o2 = o2_next.copy()
        o3 = o3_next.copy()

    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-100, 100)
    point1._offsets3d = (x1line[i*ff-1:i*ff],y1line[i*ff-1:i*ff],z1line[i*ff-1:i*ff])
    point2._offsets3d = (x2line[i*ff-1:i*ff],y2line[i*ff-1:i*ff],z2line[i*ff-1:i*ff])
    point3._offsets3d = (x3line[i*ff-1:i*ff],y3line[i*ff-1:i*ff],z3line[i*ff-1:i*ff])
    line1.set_data_3d(x1line, y1line, z1line)
    line2.set_data_3d(x2line, y2line, z2line)
    line3.set_data_3d(x3line, y3line, z3line)

Anim = ani.FuncAnimation(fig, movement, frames=int(tmax/dt)//ff, interval = 1, repeat = "false")

plt.show()