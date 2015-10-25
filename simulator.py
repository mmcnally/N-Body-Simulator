import math
import quadtree
import pickle

# bodies
all_bodies = []

# The gravitational constant G
G = 6.67428e-11

# contanst for quadtree traversal
THETA = 0.5

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 250 / AU


class Body():
    """Subclass of Turtle representing a gravitationally-acting body.

    Extra attributes:
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    """

    name = 'Body'
    mass = 0
    size = 3
    vx = vy = 0.0
    px = py = 0.0

    def attraction(self, other):
        """(Body): (fx, fy)

        Returns the force exerted upon this body by the other body.
        """
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

# curCenter [x,y]
def quarter_and_find_center(bodies,curCenter,xMult,yMult):
    maxX = maxY = 0
    for body in bodies:
        if (xMult * body.px) > (xMult * maxX):
            maxX = body.px
        if (yMult * body.py) > (yMult * maxY):
            maxY = body.py

    maxX += curCenter[0]
    maxY += curCenter[1]

    return [maxX/2,maxY/2]

def calc_diagnal(center, new_center):
    return math.sqrt( (new_center[0]-center[0])**2 + (new_center[1]-center[1])**2 )

def build_quad_tree(center,bodies):
    childGroups = {"ne":[],"nw":[],"sw":[],"se":[]}

    for body in bodies:
        if body.px >= center[0] and body.py > center[1]:
            childGroups["ne"].append(body)
        elif body.px < center[0] and body.py >= center[1]:
            childGroups["nw"].append(body)
        elif body.px <= center[0] and body.py < center[1]:
            childGroups["sw"].append(body)
        else:
            childGroups["se"].append(body)

    node = quadtree.Node(None)

    if len(childGroups["ne"]) > 0:
        if len(childGroups["ne"]) == 1:
            neNode = quadtree.Node(childGroups["ne"])
            neNode.data = childGroups["ne"][0]
            neNode.mass = childGroups["ne"][0].mass
            neNode.CoMx = childGroups["ne"][0].px
            neNode.CoMy = childGroups["ne"][0].py
        else:
            new_center = quarter_and_find_center(childGroups["ne"],center,1,1)
            neNode = build_quad_tree(new_center,childGroups["ne"])
            neNode.diagnal = neNode.calc_diagnal(center,new_center)
        node.children["ne"] = neNode

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

    tmp_body = Body()
    node.data = tmp_body

    tmp_body.mass = node.sum_children_masses()
    node.mass = tmp_body.mass

    tmp_body.px = node.calc_CoM('x',tmp_body.mass)
    node.CoMx = tmp_body.px
    tmp_body.py = node.calc_CoM('y',tmp_body.mass)
    node.CoMy = tmp_body.py

    return node


def too_far(body,other):
    numerator = other.diagnal
    denominator = calc_diagnal([body.px,body.py],[other.CoMx,other.CoMy])

    return (numerator/denominator < THETA)

def traverse_quad_tree(body,root,total):
    for child in root.children.itervalues():
        #rint child
        if child == None or child.data is body:
            continue

        if child.data.name != "Body" or too_far(body,child):
            fx, fy = body.attraction(child.data)
            total[0] += fx
            total[1] += fy
        else:
            total = traverse_quad_tree(body,child,total)

    return total

def update_bodies():
    quad_tree = build_quad_tree([0,0],all_bodies)

    timestep = 24*3600  # One day

    step = 1
    force = {}
    for body in all_bodies:
        # Add up all of the forces exerted on 'body'.
        total_fx = total_fy = 0.0

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


def build_bodies():
    # add_body(name,mass,size,color,px,py,vx,vy)
    add_body('Sun', 1988.92, 100, 'rgba(255, 204, 0, 1.0)', 0, 0, -.01, 0)
    add_body('Earth', 5.9742, 5, 'rgba(98,100,255, 1.0)', -220, 0, 0, 3)
    add_body('Moon', .5, 1, 'rgba(255,255,255, 1.0)', -230, 0, 0, 3.75)
    add_body('Venus', 10.8685, 7, 'rgba(140, 98, 2, 1.0)', 300, 0, 0, 2.5)
    add_body('mars', 3.2, 2.5, 'rgba(0, 0, 0, 1.0)', 205, 0, 1, 2.5)

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

def get_bodies():
    return all_bodies

def reset():
    build_bodies()

def update(window_width, window_height):
    update_bodies()
