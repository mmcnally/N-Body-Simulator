import math

# bodies
all_bodies = []

# The gravitational constant G
G = 6.67428e-11

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
    mass = None
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

def update_info(step, bodies):
    """(int, [Body])

    Displays information about the status of the simulation.
    """
    print('Step #{}'.format(step))
    for body in bodies:
        s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
            body.name, body.px/AU, body.py/AU, body.vx, body.vy)
        print(s)
    print()

def update_bodies():
    # TODO implmement Barnes-Hut grouping algorithm at start of every loop
    # quad_tree = bh_group()

    timestep = 24*3600  # One day

    step = 1

    step += 1

    force = {}
    for body in all_bodies:
        # Add up all of the forces exerted on 'body'.
        total_fx = total_fy = 0.0
        for other in all_bodies:
            # Don't calculate the body's attraction to itself
            if body is other: # TODO instead of looping through every body this loop should go through all the Barnes-Hut groups, recursing appropriately
                continue
            fx, fy = body.attraction(other)
            total_fx += fx
            total_fy += fy

        # Record the total force exerted.
        force[body] = (total_fx, total_fy)

    # Update velocities based upon on the force.
    for body in all_bodies:
        fx, fy = force[body]
        body.vx += fx / body.mass # * timestep
        body.vy += fy / body.mass # * timestep

        # Update positions
        body.px += body.vx # * timestep
        body.py += body.vy # * timestep



def build_bodies():
    add_body('Sun', 1988.92, 100, 'rgba(255, 204, 0, 1.0)')
    # sun = Body()
    # sun.name = 'Sun'
    # # sun.mass = 1.98892 * 10**30
    # # sun.size = sun.mass / (10 ** 28)
    # sun.mass = 1988.92
    # sun.size = 100
    # sun.px = 0
    # sun.py = 0
    # sun.vx = 0
    # sun.vy = 0
    # sun.color = 'rgba(255, 204, 0, 1.0)'

    add_body('Earth', 5.9742, 5, 'rgba(140, 98, 2, 1.0)', px=-325, vy=1)

    # earth = Body()
    # earth.name = 'Earth'
    # # earth.mass = 5.9742 * 10**24
    # # earth.size = earth.mass / (10 ** 28)
    # earth.mass = 5.9742
    # earth.size = 5
    # # earth.px = -1*AU
    # earth.px = -200
    # earth.py = 0
    # earth.vx = 1
    # earth.vy = 2
    # earth.color = 'rgba(113, 170, 255, 1.0)'

    add_body('Venus', 10.8685, 7, 'rgba(140, 98, 2, 1.0)', px=300, vy=1)

    # # Venus parameters taken from
    # # http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
    # venus = Body()
    # venus.name = 'Venus'
    # venus.mass = 10.8685
    # venus.size = 7
    # venus.px = -325
    # venus.py = 0
    # venus.vx = 0
    # venus.vy = 1
    # venus.color = 'rgba(140, 98, 2, 1.0)'

    add_body('moon', .02, 1, 'rgba(140, 98, 2, 1.0)', px=100, py=100)

    # venus = Body()
    # venus.name = 'moon'
    # venus.mass = .02
    # venus.size = 1
    # venus.px = 100
    # venus.py = 100
    # venus.vx = 0
    # venus.vy = 0
    # venus.color = 'rgba(140, 98, 2, 1.0)'

    # all_bodies.append(sun)
    # all_bodies.append(earth)
    # all_bodies.append(venus)

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
