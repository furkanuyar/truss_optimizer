#!python3

# ##----------------------------------------## #
#      Middle East Technical University        #
#       Civil Engineering Department           #
#            M. Burak Yesilyurt                #
#      Truss Optimization by Employing         #
#             Genetic Algorithms               #
# ##----------------------------------------## #

# Importing necessary modules
# To run the code below, imported python packages must be installed.


import math as m
import pylab as pl
import matplotlib as mpl
import random as rnd


def Truss_Generator(seed):
    # Random Truss Generator
    Trusses = []
    rnd.seed(seed)
    for i in range(pc):
        h1 = rnd.randrange(h1_min,h1_max,step)
        h2 = rnd.randrange(h2_min, h2_max, step)
        n_div = rnd.randrange(n_min, n_max, 1)
        div_inf = [rnd.randrange(0,3,1) for j in range(n_div)]
        Trusses.append(Truss({"h1": h1, "h2": h2, "l": l,
                              "n_div": n_div, "div_inf": div_inf}))

    lines = []
    cnt = 1
    offset = 3000
    for i in Trusses:
        off = offset * cnt
        i.plot_truss(off)
        lines += i.lines
        cnt += 1

    lc = mpl.collections.LineCollection(lines, linewidths=2)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(1)
    input()


    return Trusses

class Truss:
        # Truss Parameters for DNA Creation
        # h1, h2, l (in mm)
        # n_div (integer)
        def __init__(self, param):
            self.h1 = param["h1"]
            self.h2 = param["h2"]
            self.l = param["l"]
            self.n_div = param["n_div"]
            div_inf = param["div_inf"]
            self.node_cr()
            self.elem_cr(div_inf)

        def node_cr(self):
            # Creation of Nodal Information

            top_angle = m.atan((self.h2 - self.h1) * 2 / self.l)
            step_x = self.l / self.n_div / 2
            step_z = (self.h2 - self.h1) / self.n_div

            nodes = []

            x = 0
            n = 1
            for i in range(2 * self.n_div + 1):
                nodes.append([x, 0])
                n += 1
                x += step_x

            z = self.h1
            x = 0
            for i in range(self.n_div + 1):
                nodes.append([x, z])
                z += step_z
                x += step_x
                n += 1

            z -= 2 * step_z
            for i in range(0, self.n_div):
                nodes.append([x, z])
                z -= step_z
                x += step_x
                n += 1

            self.n_coord = nodes
            self.node_count = n

        def elem_cr(self, div_inf):
            # Creation of Truss Elements

            # Truss Top and Bottom Chords
            n = 1
            elem = []
            for j in range(2):
                for i in range(2 * self.n_div):
                    node_i = n
                    node_j = n + 1
                    elem.append([node_i, node_j])
                    n += 1
                n += 1

            # Truss Posts
            n = 1
            for i in range(2 * self.n_div + 1):
                node_i = n
                node_j = 2 * self.n_div + 1 + n
                elem.append([node_i, node_j])
                n += 1

            # Truss Diagonals
            left = div_inf
            right = []
            for i in div_inf[::-1]:
                if i == 1:
                    right.append(0)
                elif i == 0:
                    right.append(1)
                else:
                    right.append(i)

            self.dia_orient = left + right

            n = 1
            for i in range(2 * self.n_div):
                orient = self.dia_orient[i]

                if orient == 1:
                    node_i = n + 2 * self.n_div + 1
                    node_j = n + 1
                    elem.append([node_i, node_j])
                elif orient == 0:
                    node_i = n
                    node_j = n + 2 * self.n_div + 2
                    elem.append([node_i, node_j])
                else:
                    node_i = n + 2 * self.n_div + 1
                    node_j = n + 1
                    elem.append([node_i, node_j])
                    node_i = n
                    node_j = n + 2 * self.n_div + 2
                    elem.append([node_i, node_j])
                n += 1
            self.elements = elem

        def plot_truss(self, offset):
            lines = []
            for i in self.elements:
                node_i = i[0]
                node_j = i[1]
                coord_ix = self.n_coord[node_i - 1][0]
                coord_iz = self.n_coord[node_i - 1][1] + offset
                coord_jx = self.n_coord[node_j - 1][0]
                coord_jz = self.n_coord[node_j - 1][1] + offset
                coord_i = (coord_ix, coord_iz)
                coord_j = (coord_jx, coord_jz)
                lines.append([coord_i, coord_j])
            self.lines = lines

        def member(self):
            pass

class Steel:
        def __init__(self, fy, fu, e, gamma, alpha):
            self.Fy = fy
            self.Fu = fu
            self.E = e
            self.gamma = gamma
            self.alpha = alpha

# Steel Catalogue
catalogue = {"S235":Steel(235,360,200000,7850,1.17e-5), "S275": Steel(275,430,200000,7850,1.17e-5),
"S355": Steel(355,510,200000,7850,1.17e-5), "S450": Steel(440,550,200000,7850,1.17e-5)}


# Input Card

# Dimensional Constraints
h1_min = 1500  # Minimum Edge Height in mm
h1_max = 1800  # Maximum Edge Height in mm
h2_min = 1900  # Minimum Peak Height in mm
h2_max = 2400  # Maximum Peak Height in mm
step = 100  # Variation of Heights in mm
l = 29000  # Span Length in mm
n_min = 6  # Minimum Number of Divisions
n_max = 10  # Maximum Number of Divisions

# Population and Genetic Diversity Characteristics
pc = 100  # Population Count
mp = 1  # Mutation Probability

# Material and Section Properties
mat = catalogue["S275"]  # Available Material Properties are S235, S275, S355 and S450

#- W for wide flange,
# O for CHS,
# K for RHS & SHS,
# L for Angle
# C for Channel,
# DL for Double Angle,
# DC for Double Channel,

tc_mem = "W"  # Preferred Sectional Shape for Truss Chords For Now only W sections available.
tp_mem = "O"  # Preferred Sectional Shape for Truss Posts - For Now only O, K, C, L sections available
td_mem = "O"  # Preferred Sectional Shape for Truss Posts - For Now only O, K, C, L sections available


Truss_Generator(2)

#class Member:
#    def __init__(self):


# Structural Analysis

# for i in Tru:











