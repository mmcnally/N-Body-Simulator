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


@app.route('/get_all_bodies')
def get_all_bodies():
    AU = (149.6e6 * 1000)

    sun = simulator.Body()
    sun.name = 'Sun'
    sun.mass = 1.98892 * 10**30
    sun.size = sun.mass / (10 ** 28)
    sun.px = 0
    sun.py = 0
    sun.vx = 0
    sun.vy = 0
    sun.color = 'rgba(255, 204, 0, 1.0)'

    earth = simulator.Body()
    earth.name = 'Earth'
    earth.mass = 5.9742 * 10**24
    earth.size = earth.mass / (10 ** 28)
    earth.px = -1*AU
    earth.py = 0
    earth.vx = 0
    earth.vy = 29.783 * 1000
    sun.color = 'rgba(113, 170, 255, 1.0)'

    x = [{"name":sun.name, "x":sun.px, "y":sun.py},{"name":earth.name, "x":earth.px, "y":earth.py}]
    return json.dumps(x)

@app.route('/<path:path>')
def index(path):
    print "asdf"
    return send_from_directory('',path)

if __name__ == '__main__':
    app.debug = True
    app.run()
