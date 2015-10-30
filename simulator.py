import math
import quadtree
import pickle

# bodies currently being simulated
all_bodies = []

# The gravitational constant G
G = 6.67428e-11

# contanst for quadtree traversal
THETA = 0.5

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 250 / AU


class Body():

    name = 'Body' # id of planet

    # default parameters of planets
    mass = 0
    size = 3
    vx = vy = 0.0
    px = py = 0.0

    # calculates the amount of attraction between a planet and "other" (either a planet or a node due to B&H)
    def attraction(self, other):

        # Report an error if the other object is the same as this one.
        if self is other:
            raise ValueError("Attraction of object %r to itself requested"
                             % self.name)

        # Compute the distance of the other body.
        sx, sy = self.px, self.py
        ox, oy = other.px, other.py
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)

        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            raise ValueError("Collision between objects %r and %r"
                             % (self.name, other.name))

        # Compute the force of attraction
        f = self.mass * other.mass / (d**2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy

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

# a^2 + b^2 = c^2 calculation
def calc_diagnal(center, new_center):
    return math.sqrt( (new_center[0]-center[0])**2 + (new_center[1]-center[1])**2 )

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
    node = quadtree.Node(None)

    '''
    All four of the if statements below do the same thing, but for different quadrants.
    TODO: extract this functionality into a helper funtion in quadtree.py to remove redunancy (pass in what quadrant & other info needed)
    '''
    # if the length of the list of children for the quadrant is greater than 0 something needs to be done.
    if len(childGroups["ne"]) > 0:
        # if there is only one child in this quadrant
        if len(childGroups["ne"]) == 1:
            # get the respective quadrant's node's chilren from the tree
            neNode = quadtree.Node(childGroups["ne"])
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
            nwNode = quadtree.Node(childGroups["nw"][0])
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
            swNode = quadtree.Node(childGroups["sw"][0])
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
            seNode = quadtree.Node(childGroups["se"][0])
            seNode.data = childGroups["se"][0]
            seNode.mass = childGroups["se"][0].mass
            seNode.CoMx = childGroups["se"][0].px
            seNode.CoMy = childGroups["se"][0].py
        else:
            new_center = quarter_and_find_center(childGroups["se"],center,1,-1)
            seNode = build_quad_tree(new_center,childGroups["se"])
            seNode.diagnal = seNode.calc_diagnal(center,new_center)
        node.children["se"] = seNode


    # after all recusion is copmleted, create the root node & its pseudo-body
    tmp_body = Body()
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

"""
This function calculates if the current body is far enough away from a group. If it is far enough away the
groups information (mass, center of mass) can be used, instead of its composit planets information, to make the
force calculation.
"""
def too_far(body,other):

    numerator = other.diagnal
    denominator = calc_diagnal([body.px,body.py],[other.CoMx,other.CoMy])

    # theta is a global threshold (how far does the body need to be away from the group before the group's information can be used)
    return (numerator/denominator < THETA)

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
        if child.data.name != "Body" or too_far(body,child):
            # get force excerted
            fx, fy = body.attraction(child.data)
            # add it to the sum
            total[0] += fx
            total[1] += fy
        # otherwise go deeper into the tree
        else:
            total = traverse_quad_tree(body,child,total)

    return total

'''
this method updates the positionf of every body by calculating the forces the body experiences, then updating its position and velocity.
'''
def update_bodies():
    quad_tree = build_quad_tree([0,0],all_bodies) # builds the quad-tree

    timestep = 24*3600  # One day

    step = 1
    force = {}
    # for every body
    for body in all_bodies:
        # Add up all of the forces exerted on 'body'.
        total_fx = total_fy = 0.0

        # traverse_quad_tree find the total force on the current body with respect to the other bodies and groups (if the body is far enough away from the group)
        total = traverse_quad_tree(body,quad_tree,[0,0])

        # Record the total force exerted.
        force[body] = (total[0], total[1])

    # Update velocities based upon on the force.
    for body in all_bodies:
        fx, fy = force[body]
        body.vx += fx / body.mass # * timestep
        body.vy += fy / body.mass # * timestep

        # Update positions
        body.px += body.vx # * timestep
        body.py += body.vy # * timestep


'''
This function build the default bodies shown in the app
'''
def build_bodies():

    # add_body(name,mass,size,color,px,py,vx,vy)
    add_body('Sun', 1988.92, 100, 'rgba(255, 204, 0, 1.0)', 0, 0, -.01, 0)
    add_body('Earth', 5.9742, 5, 'rgba(98,100,255, 1.0)', -220, 0, 0, 3)
    add_body('Moon', .5, 1, 'rgba(255,255,255, 1.0)', -230, 0, 0, 3.75)
    add_body('Venus', 10.8685, 7, 'rgba(140, 98, 2, 1.0)', 300, 0, 0, 2.5)


'''
This function handles the creation of a body and sets default values if they are not given
'''
def add_body(name, mass, size, color, px=0, py=0, vx=0, vy=0):
    bod = Body()
    bod.name = name
    bod.mass = mass
    bod.size = size
    bod.px = px
    bod.py = py
    bod.vx = vx
    bod.vy = vy
    bod.color = color
    all_bodies.append(bod)

'''
Gets all the bodies within the app
'''
def get_bodies():
    return all_bodies

'''
Reset, rebuild all default bodies
'''
def reset():
    build_bodies()

'''
Update runs the model one time step
'''
def update(window_width, window_height):
    update_bodies()
