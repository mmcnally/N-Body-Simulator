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

app = Flask(__name__, static_url_path='/Users/Computer/Copy/Hackathon/N-Body-Simulator')


@app.route('/update_all_bodies')
def update_all_bodies():
    simulator.update()
    bodies = simulator.get_bodies()

    all_bodies_update = []
    for body in bodies:
        all_bodies_update.append({"name":body.name, "px":body.px, "py":body.py})

    print len(all_bodies_update)
    return json.dumps(all_bodies_update)

@app.route('/get_all_bodies')
def get_all_bodies():
    simulator.build_bodies()
    bodies = simulator.get_bodies()

    all_bodies = []
    for body in bodies:
        all_bodies.append({"name":body.name, "px":body.px, "py":body.py, "size":body.size, "color":body.color})

    return json.dumps(all_bodies)

@app.route('/<path:path>')
def index(path):
    print "asdf"
    return send_from_directory('',path)

if __name__ == '__main__':
    app.debug = True
    app.run()
