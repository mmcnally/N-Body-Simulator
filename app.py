# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~
    A simple application that shows how Flask and jQuery get along.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, jsonify, render_template, request, send_from_directory
import simulator
import json
import random
import datetime
import time
import math

app = Flask(__name__, static_url_path='/Users/Computer/Copy/Hackathon/N-Body-Simulator')

@app.route('/update_all_bodies/<int:width>/<int:height>')
def update_all_bodies(width,height):
    simulator.update(width,height)
    bodies = simulator.get_bodies()

    all_bodies_update = []
    for body in bodies:
        all_bodies_update.append({"name":body.name, "px":body.px, "py":body.py})

    return json.dumps(all_bodies_update)


@app.route('/get_all_bodies')
def get_all_bodies():
    if len(simulator.get_bodies())==0:
        simulator.build_bodies()

    bodies = simulator.get_bodies()

    all_bodies = []
    for body in bodies:
        all_bodies.append({"name":body.name, "px":body.px, "py":body.py, "size":body.size, "color":body.color})

    return json.dumps(all_bodies)

@app.route('/add_body/<xPos>/<yPos>/<xVel>/<yVel>/<size>')
def add_body(xPos,yPos,xVel,yVel,size):
    newId = 'newBody%s' % (datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f"))
    newMass = random.random() * 11
    newSize = size
    newColor = 'rgba(%i,%i,%i,1.0)' % (random.random() * 255,random.random() * 255,random.random() * 255)
    newPx = int(float(xPos))
    newPy = int(float(yPos))
    newVx = int(float(xVel)) / 20
    newVy = int(float(yVel)) / 20

    simulator.add_body(newId,newMass,newSize,newColor,newPx,newPy,newVx,newVy)

    body = simulator.all_bodies[len(simulator.all_bodies)-1]

    return json.dumps({"name":body.name, "px":body.px, "py":body.py, "size":body.size, "color":body.color})

@app.route('/reset_bodies')
def reset_bodies():

    bodies = simulator.get_bodies()

    all_bodies_Ids = []
    for body in bodies:
        all_bodies_Ids.append({"name":body.name})

    simulator.all_bodies = [];

    return json.dumps(all_bodies_Ids)


@app.route('/<path:path>')
def index(path):
    return send_from_directory('',path)

if __name__ == '__main__':
    app.debug = True
    app.run()
