import math
import simulator

'''
This is a basic quadtree class. it defines what nodes will store as well as giving some helpful functionality used when building the quad-tree
TODO: a lot of functionality that should be encapsulated in this class is in simulator.py EXTRACT IT!!!
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






"""
breaks the current field into 4 quadrants, and finds its center (so planets can be sorted into groups)
curCenter [x,y]
xMult and yMult take values 1 or -1, and are used so only two if statements are needed
they effectively flip the comparison opperator [1*a > 1*b -> -1*a < -1*b] so max is actually min when calulating for negative quadrants
"""
def quarter_and_find_center(bodies,curCenter,xMult,yMult):
    maxX = maxY = 0
    # for all bodies find the maxX and maxY (the otehr corner of the quadrant)
    for body in bodies:
        if (xMult * body.px) > (xMult * maxX):
            maxX = body.px
        if (yMult * body.py) > (yMult * maxY):
            maxY = body.py

    # (curCenter + maxX&Y) / 2 is the new center
    maxX += curCenter[0]
    maxY += curCenter[1]

    return [maxX/2,maxY/2]








'''
This is part of our implementation of the Barnes and Hut Algorithm, a good description of how this algorihm works can be found here.
    http://arborjs.org/docs/barnes-hut

This function build a quad-tree, used within the B&H algorithm, by recursively breaking the space within the app into quadrants. Each quadrant is associated with a mass (the sum of all planets within the quadrant)
and a center of mass (calculated with respect to position and mass of all planets within quadrant). The function recursively breaks ever quadrant into 4 more quadrants until each quadrant
only contains 1 or 0 nodes. It then builds a quad-tree from the bottom up. Each leaf is a planet, each internal node is a psudo-body meaning it has a mass and center of mass that can be
accessed as if it was a real body for calulations later in the B&H algorithm
'''
def build_quad_tree(center,bodies):
    # initialize a dictonary to determine how many children there are in each quadrant
    childGroups = {"ne":[],"nw":[],"sw":[],"se":[]}

    # put each child in its resepctive quadrant
    for body in bodies:
        if body.px >= center[0] and body.py > center[1]:
            childGroups["ne"].append(body)
        elif body.px < center[0] and body.py >= center[1]:
            childGroups["nw"].append(body)
        elif body.px <= center[0] and body.py < center[1]:
            childGroups["sw"].append(body)
        else:
            childGroups["se"].append(body)

    # create the node of the quad-tree
    node = Node(None)

    '''
    All four of the if statements below do the same thing, but for different quadrants.
    TODO: extract this functionality into a helper funtion in quadtree.py to remove redunancy (pass in what quadrant & other info needed)
    '''
    # if the length of the list of children for the quadrant is greater than 0 something needs to be done.
    if len(childGroups["ne"]) > 0:
        # if there is only one child in this quadrant
        if len(childGroups["ne"]) == 1:
            # get the respective quadrant's node's chilren from the tree
            neNode = Node(childGroups["ne"])
            # set the nodes data to the bodies data (and store the body itself)
            neNode.data = childGroups["ne"][0]
            neNode.mass = childGroups["ne"][0].mass
            neNode.CoMx = childGroups["ne"][0].px
            neNode.CoMy = childGroups["ne"][0].py
        #otherwise find a new center, and create a new node, calculate it's diagnal length and recurse on this quadrant
        else:
            new_center = quarter_and_find_center(childGroups["ne"],center,1,1)
            neNode = build_quad_tree(new_center,childGroups["ne"])
            neNode.diagnal = neNode.calc_diagnal(center,new_center)
        # set the child to the new node (either a planet or a group)
        node.children["ne"] = neNode

    # same as 1st if but for the north west quadrant
    if len(childGroups["nw"]) > 0:
        if len(childGroups["nw"]) == 1:
            nwNode = Node(childGroups["nw"][0])
            nwNode.data = childGroups["nw"][0]
            nwNode.mass = childGroups["nw"][0].mass
            nwNode.CoMx = childGroups["nw"][0].px
            nwNode.CoMy = childGroups["nw"][0].py
        else:
            new_center = quarter_and_find_center(childGroups["nw"],center,-1,1)
            nwNode = build_quad_tree(new_center,childGroups["nw"])
            nwNode.diagnal = nwNode.calc_diagnal(center,new_center)
        node.children["nw"] = nwNode

    # same as 1st if but for the south west quadrant
    if len(childGroups["sw"]) > 0:
        if len(childGroups["sw"]) == 1:
            swNode = Node(childGroups["sw"][0])
            swNode.data = childGroups["sw"][0]
            swNode.mass = childGroups["sw"][0].mass
            swNode.CoMx = childGroups["sw"][0].px
            swNode.CoMy = childGroups["sw"][0].py
        else:
            new_center = quarter_and_find_center(childGroups["sw"],center,-1,-1)
            swNode = build_quad_tree(new_center,childGroups["sw"])
            swNode.diagnal = swNode.calc_diagnal(center,new_center)
        node.children["sw"] = swNode

    # same as 1st if but for the south east quadrant
    if len(childGroups["se"]) > 0:
        if len(childGroups["se"]) == 1:
            seNode = Node(childGroups["se"][0])
            seNode.data = childGroups["se"][0]
            seNode.mass = childGroups["se"][0].mass
            seNode.CoMx = childGroups["se"][0].px
            seNode.CoMy = childGroups["se"][0].py
        else:
            new_center = quarter_and_find_center(childGroups["se"],center,1,-1)
            seNode = build_quad_tree(new_center,childGroups["se"])
            seNode.diagnal = seNode.calc_diagnal(center,new_center)
        node.children["se"] = seNode



    # after all recusion is completed, create the root node & its pseudo-body
    tmp_body = simulator.Body()
    node.data = tmp_body

    # calulate the total sum of all planets masses
    tmp_body.mass = node.sum_children_masses()
    node.mass = tmp_body.mass

    # calculate the roots cetner of mass
    tmp_body.px = node.calc_CoM('x',tmp_body.mass)
    node.CoMx = tmp_body.px
    tmp_body.py = node.calc_CoM('y',tmp_body.mass)
    node.CoMy = tmp_body.py

    # return the root of the quad-tree
    return node








'''
This method sums the total force excerted on a body.
It does not calculate anythin if the curren node has no cildren or the node is the body itself

It does this by traversing the quad-tree:
    IF the current node on the tree has only one body (its a leaf) use that body's info to calulate force
        OR the current node is far enough away from the current body use its Center of Mass and mass to calculate force
    ELSE recurse down the quad-tree into smaller quadrants and recompute.
'''
def traverse_quad_tree(body,root,total):
    # for all children
    for child in root.children.itervalues():
        # if there is no data or the child is the body itself skip this itteration
        if child == None or child.data is body:
            continue

        # if the child is a body or is far enough away from the current body calculate force
        # TODO -- move too_far into either body of quadree
        if child.data.name != "Body" or simulator.too_far(body,child):
            # get force excerted
            # TODO -- move body out of simulator
            fx, fy = body.attraction(child.data)
            # add it to the sum
            total[0] += fx
            total[1] += fy
        # otherwise go deeper into the tree
        else:
            total = traverse_quad_tree(body,child,total)

    return total
