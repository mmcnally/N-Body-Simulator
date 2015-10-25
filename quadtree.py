import math

class Node(object):
    def __init__(self, data):
        self.data = data
        self.mass = 0
        self.CoMx = 0
        self.CoMy = 0
        self.diagnal = 0
        self.children = {"ne": None,"nw": None,"sw": None,"se": None}

    def add_child(self, obj):
        self.children.append(obj)

    def sum_children_masses(self):
        total_mass = 0
        for child in self.children.itervalues():
            if child != None:
                total_mass += child.mass
        return total_mass

    def calc_CoM(self,axis,mass):
        total_CoM = 0
        for child in self.children.itervalues():
            if child != None:
                if axis == 'x':
                    total_CoM += child.mass * child.CoMx
                if axis == 'y':
                    total_CoM += child.mass * child.CoMy

        if mass == 0:
            return 0
        else:
            return total_CoM/mass

    def calc_diagnal(self, center, new_center):
        return math.sqrt( (new_center[0]-center[0])**2 + (new_center[1]-center[1])**2 )
