import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Vector class

class vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __truediv__(self, num):
        x = self.x / num
        y = self.y / num
        z = self.z / num
        return vector(x, y, z)
    
    def __mul__(self, num):
        x = self.x * num
        y = self.y * num
        z = self.z * num
        return vector(x, y, z)
    
    def __rmul__(self, num):
        return self * num
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return vector(x, y, z)

    def __neg__(self):
        return vector(-self.x, -self.y, -self.z)
    
    def mag(self):
        return mag(self)
    
    def mag2(self):
        return mag2(self)
    
    def hat(self):
        return hat(self)

    def dot(self, other):
        return dot(self, other)

    def cross(self, other):
        return cross(self, other)

# Vector functions

def mag(vec):
    return np.sqrt(vec.x**2 + vec.y**2 + vec.z**2)

def mag2(vec):
    return mag(vec)**2

def hat(vec):
    return vec/mag(vec)

def dot(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def cross(v1, v2):
    a1 = v1.x
    a2 = v1.y
    a3 = v1.z
    b1 = v2.x
    b2 = v2.y
    b3 = v2.z

    return vector(a2*b3-a3*b2, a3*b1-a1*b3, a1*b2-a2*b1)

# functions

def lvector(vec):
    return [vec.x, vec.y, vec.z]

def array(vec):
    return np.array(lvector(vec))

def vlist(list):
    return vector(list[0], list[1], list[2])

def findvalue(list, n):
    plist = []
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] == n:
                plist.append(i)
    return plist

# find the plane crossing the midpoint between point r1 and r2
def midplane(r1, r2):
    n = (r2 - r1)/2
    return n

# find the intersection of plane given 3 points
def edge(r1, r2, r3):
    n1 = midplane(r1, r2)
    n2 = midplane(r1, r3)
    v = n1.cross(n2)
    t = n1.cross(v)

    k = ((n2-n1).dot(n2.hat))/(t.dot(n2.hat)) 

    r_0 = r1 + n1 + k*t
    
    return r_0, v

#find the intersction of two given lines
def cpoint(r1, v1, r2, v2):
    p = v1.hat-v2.hat
    q = v1.hat+v2.hat
    d = r2 - r1
    l = dot(v2.hat, v1.hat)
    t = 1/mag2(p) * (dot(d, p) - dot(v1.hat, p) * (dot(d, q))/(1+l))
    return r2 + t*v2.hat

# class

# crystal unit class
class cunit:
    # initializing
    def __init__(self, r, b1, b2, b3):
        self.r = r
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
    
    # calculating point vector from given basis and coefficient
    def point(self, c, v):
        return c + self.b1 * v.x  + self.b2 * v.y + self.b3 * v.z
    
    # calculate the edge of polyhedron using a point and directions to check
    def buildedge(self, c, v1, v2):
        r, v = edge(self.point(c), self.point(c+v1), self.point(c+v2))
        return r, v
    
    # calculate the vertices using the edge calculated
    # def vertice(self, c, v, v1, v2, plot):
    #     r_1, v_1 = self.buildedge(c, v, v1)
    #     r_2, v_2 = self.buildedge(c, v, v2)
    #     pp = cpoint(r_1, v_1, r_2, v_2)
    #     # points(pos = [pp], radius = 3, color = color.red)
    #     plt.scatter3D(pp.x, pp.y, pp.z)

    def createvlist(self, list, c, v1, v2, v3):
        list.append(lvector(self.point(c, v1)))
        list.append(lvector(self.point(c, v2)))
        list.append(lvector(self.point(c, v3)))
        list.append(lvector(self.point(c, v1+v2)))
        list.append(lvector(self.point(c, v1+v3)))
        list.append(lvector(self.point(c, v2+v3)))
        list.append(lvector(self.point(c, v1+v2+v3)))
    
    def sector(self, c):
        v1 = vector(1, 0, 0)
        v2 = vector(0, 1, 0)
        v3 = vector(0, 0, 1)
        plist = [lvector(c)]
        self.createvlist(plist, c, v1, v2, v3)
        self.createvlist(plist, c, v1, v2, -v3)
        self.createvlist(plist, c, v1, -v2, v3)
        self.createvlist(plist, c, v1, -v2, -v3)
        self.createvlist(plist, c, -v1, v2, v3)
        self.createvlist(plist, c, -v1, v2, -v3)
        self.createvlist(plist, c, -v1, -v2, v3)
        self.createvlist(plist, c, -v1, -v2, -v3)
        return plist

    # create one cell with a center point.
    def buildcell(self, c):

        voronoi = Voronoi(self.sector(c))
        for i in range(len(findvalue(voronoi.ridge_points, 0))):
            t = voronoi.ridge_vertices[findvalue(voronoi.ridge_points, 0)[i]]
            for j in range(len(t)):
                p = t[j]
                if j+1 != len(t):
                    p1 = vlist(voronoi.vertices[p])
                    p2 = vlist(voronoi.vertices[t[j+1]])
                else:
                    p1 = vlist(voronoi.vertices[p])
                    p2 = vlist(voronoi.vertices[t[0]])
                # cylinder(pos = p1, axis = p2 - p1, radius = 0.005, color = color.blue)
                x = [p1.x, p2.x]
                y = [p1.y, p2.y]
                z = [p1.z, p2.z]
                plt.plot(x, y, z, color = 'blue')
            for j in range(1, len(t)-1):
                p1 = t[j]
                p2 = t[j+1]

                v0 = vlist(voronoi.vertices[t[0]])
                v1 = vlist(voronoi.vertices[p1])
                v2 = vlist(voronoi.vertices[p2])

                x = [v0.x, v1.x, v2.x]
                y = [v0.y, v1.y, v2.y]
                z = [v0.z, v1.z, v2.z]

                # v1 = vertex( pos = vlist(voronoi.vertices[t[0]]), opacity = 0.5 )
                # v2 = vertex( pos = vlist(voronoi.vertices[p1]), opacity = 0.5 )
                # v3 = vertex( pos = vlist(voronoi.vertices[p2]), opacity = 0.5 )
                # T = triangle( vs = [v1, v2, v3] )
                verts = [list(zip(x, y, z))]
                srf = Poly3DCollection(verts, alpha = .1, facecolor = 'blue')
                plt.gca().add_collection3d(srf)


    # create multiple cells with given size
    def gridcell(self, size):
        fig = plt.figure()
        ax = plt.axes(projection = '3d')
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    c = vector(i, j, k)
                    p = self.point(self.r, c)
                    ax.scatter3D(p.x, p.y, p.z, color = 'red')
                    self.buildcell(self.point(self.r, c))
        plt.show()

#the origin point
O = vector(0, 0, 0)

# the bases
b1 = 0.5 * vector(1, -1, -1)
b2 = 0.5 * vector(-1, 1, -1)
b3 = 0.5 * vector(-1, -1, 1)

cu1 = cunit(O, b1, b2, b3)

# using bigger number creates multiple cells
cu1.gridcell(1)