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
        f = G * self.mass * other.mass / (d**2)

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

def loop(bodies):
    """([Body])

    Never returns; loops through the simulation, updating the
    positions of all the provided bodies.
    """
    # TODO implmement Barnes-Hut grouping algorithm at start of every loop
    # quad_tree = bh_group()

    timestep = 24*3600  # One day

    step = 1
    while True:
        update_info(step, bodies)
        step += 1

        force = {}
        for body in bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other: # TODO instead of looping through every body this loop should go through all the Barnes-Hut groups, recursing appropriately
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep
            
            
def updateBodies():
    # TODO implmement Barnes-Hut grouping algorithm at start of every loop
    # quad_tree = bh_group()

    timestep = 24*3600  # One day

    step = 1
    
    update_info(step)
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
        body.vx += fx / body.mass * timestep
        body.vy += fy / body.mass * timestep

        # Update positions
        body.px += body.vx * timestep
        body.py += body.vy * timestep



def build_bodies():
    sun = Body()
    sun.name = 'Sun'
    # sun.mass = 1.98892 * 10**30
    # sun.size = sun.mass / (10 ** 28)
    sun.mass = 1.98892 * 10**30
    sun.size = 100
    sun.px = 0
    sun.py = 0
    sun.vx = 0
    sun.vy = 0
    sun.color = 'rgba(255, 204, 0, 1.0)'

    earth = Body()
    earth.name = 'Earth'
    # earth.mass = 5.9742 * 10**24
    # earth.size = earth.mass / (10 ** 28)
    earth.mass = 5.9742 * 10**24
    earth.size = 5
    # earth.px = -1*AU
    earth.px = -200
    earth.py = 0
    earth.vx = 1
    earth.vy = 2
    earth.color = 'rgba(113, 170, 255, 1.0)'

    all_bodies.append(sun)
    all_bodies.append(earth)
    # Venus parameters taken from
    # http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
    # venus = Body()
    # venus.name = 'Venus'
    # venus.mass = 4.8685 * 10**24
    # venus.size = venus.mass / (10 ** 28)
    # venus.px = 0.723 * AU
    # venus.vy = -35.02 * 1000

def get_bodies():
    return all_bodies

def update():
    if len(all_bodies) > 0:
        # bodies have been initialized
        updateBodies()
    else:
        # need to create the bodies
        buildBodies()
