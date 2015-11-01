# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, send_from_directory
import json
import random
import datetime
import time
import math
import os

import simulator

'''
Applications needs static path to 'N-Body-Simulator'
directory in order to function properly
'''
STATIC_PATH = os.getcwd() # EXAMPLE: /Users/Computer/Copy/Hackathon/N-Body-Simulator

app = Flask(__name__, static_url_path=STATIC_PATH)


# route used to update body positions after they have been added initially
@app.route('/update_all_bodies/<int:width>/<int:height>')
def update_all_bodies(width,height):
    simulator.update(width,height) # runs one loop of the simulation to get next position of planets
    bodies = simulator.get_bodies() # gets the plant data (name, xPos, yPos)

    # format data to be JSON dumpable
    all_bodies_update = []
    for body in bodies:
        all_bodies_update.append({"name":body.name, "px":body.px, "py":body.py})

    # return planet data
    return json.dumps(all_bodies_update)


# route used to creat the planets (if necessary) and get all their data to draw them initially
@app.route('/get_all_bodies')
def get_all_bodies():
    # if there are no bodies, recreate the default bodies
    if len(simulator.get_bodies())==0:
        simulator.build_bodies()

    bodies = simulator.get_bodies() # gets all the plant data (name, xPos, yPos, size, and color)

    # format data to be JSON dumpable
    all_bodies = []
    for body in bodies:
        all_bodies.append({"name":body.name, "px":body.px, "py":body.py, "size":body.size, "color":body.color})

    # return planet data
    return json.dumps(all_bodies)


# routse used to create new bodies when user clicks
@app.route('/add_body/<xPos>/<yPos>/<xVel>/<yVel>/<size>')
def add_body(xPos,yPos,xVel,yVel,size):
    newId = 'newBody%s' % (datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")) # each body needs a unique ID (date+time with milisecond data does this well)
    newMass = random.random() * 11 # generate a random mass (size and mass are decoupled as of now... will update later)
    newSize = size # the radius of the planet
    newColor = 'rgba(%i,%i,%i,1.0)' % (random.random() * 255,random.random() * 255,random.random() * 255) # random color of planet
    # position is based on where mouse position on mousedown
    newPx = int(float(xPos))
    newPy = int(float(yPos))
    # velocity is based on the difference of mouse position on mousedown and mouseup
    newVx = int(float(xVel)) / 20
    newVy = int(float(yVel)) / 20

    # adds the new body
    simulator.add_body(newId,newMass,newSize,newColor,newPx,newPy,newVx,newVy)

    # gets the last body (the one that was just added)
    body = simulator.all_bodies[len(simulator.all_bodies)-1]

    # retur the new bodies information in JSON format
    return json.dumps({"name":body.name, "px":body.px, "py":body.py, "size":body.size, "color":body.color})


# route used to reset the app (remove all user created bodies and reset the default bodies to initial pos & vel)
@app.route('/reset_bodies')
def reset_bodies():
    # gets all the bodies (necessary because we need their name to remove them from the D3 chart)
    bodies = simulator.get_bodies()

    # format data to be JSON dumpable
    all_bodies_Ids = []
    for body in bodies:
        all_bodies_Ids.append({"name":body.name})

    # clears all bodies from app
    simulator.all_bodies = [];

    # returns JSON data of all the past bodies (so they can be removed)
    return json.dumps(all_bodies_Ids)

# route used to render the application
@app.route('/<path:path>')
def index(path):
    # sends all the files from the directory (this is the index file as well as the back end and REST API etc)
    return send_from_directory('',path)

# runs the simulator
if __name__ == '__main__':
        app.run()
