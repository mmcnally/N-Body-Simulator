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

    """
    This function calculates if the current body is far enough away from a group.
    If it is far enough away the groups information (mass, center of mass) can be used,
    instead of its composit planets information, to make the force calculation.
    """
    def too_far(self, other):
        numerator = other.diagnal
        denominator = calc_diagnal([self.px,self.py],[other.CoMx,other.CoMy])

        # theta is a global threshold (how far does the body need to be away from the
        # group before the group's information can be used)
        return (numerator/denominator < THETA)


    # calculates the amount of attraction between a planet and "other"
    # (either a planet or a node due to B&H)
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


# a^2 + b^2 = c^2 calculation
def calc_diagnal(center, new_center):
    return math.sqrt( (new_center[0]-center[0])**2 + (new_center[1]-center[1])**2 )




'''
this method updates the positionf of every body by calculating the forces the body experiences, then updating its position and velocity.
'''
def update_bodies():
    quad_tree = quadtree.build_quad_tree([0,0],all_bodies) # builds the quad-tree
    timestep = 24*3600  # One day

    step = 1
    force = {}
    # for every body
    for body in all_bodies:
        # Add up all of the forces exerted on 'body'.
        total_fx = total_fy = 0.0

        # traverse_quad_tree find the total force on the current body with respect to the other bodies and groups (if the body is far enough away from the group)

        total = quadtree.traverse_quad_tree(body,quad_tree,[0,0])

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
