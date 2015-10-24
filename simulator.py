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
    
# def log_normalize_bodies():
#     for body in all_bodies:
        
    

def update_bodies():
    # TODO implmement Barnes-Hut grouping algorithm at start of every loop
    # quad_tree = bh_group()

    timestep = 24*3600  # One day

    step = 1
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
    add_body('Earth', 5.9742, 5,'rgba(98,100,255, 1.0)', px=-220, vy=3)
    add_body('Venus', 10.8685, 7, 'rgba(140, 98, 2, 1.0)', px=300, vy=2.5)

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
    
