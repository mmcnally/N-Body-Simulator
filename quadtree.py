import math
'''
This is a basic quadtree class. it defines what nodes will store as well as giving some helpful functionality used when building the quad-tree
TODO: a lof of functionality that should be encapsulated in this class is in simulator.py EXTRACT IT!!!
'''
class Node(object):
    def __init__(self, data):
        self.data = data # the body object istelf (this is set to 'Body' if it is not a leaf node [aka not a planet])
        self.mass = 0 # mass of the node (sum of all bodies held within it)
        self.CoMx = 0 # Center of Mass with respect to the X axis
        self.CoMy = 0 # Center of Mass with respect to the Y axis
        self.diagnal = 0 # The length of the diagnal of this quadrant (used to calculate if the quadrant is far enough away from a planet to use for calculations)
        self.children = {"ne": None,"nw": None,"sw": None,"se": None} # each internal node has up to 4 children (one for each quadrant)

    def add_child(self, obj):
        self.children.append(obj)

    # sums the mass of all children of a node
    def sum_children_masses(self):
        total_mass = 0
        for child in self.children.itervalues():
            if child != None:
                total_mass += child.mass
        return total_mass

    # caldulates the x and y center of mass for the node
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

    # a^2 + b^2 = c^2 calculation
    def calc_diagnal(self, center, new_center):
        return math.sqrt( (new_center[0]-center[0])**2 + (new_center[1]-center[1])**2 )
