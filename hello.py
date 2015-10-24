from flask import Flask, jsonify, render_template, request
import simulator
app = Flask(__name__)

@app.route("/")
def runSimulation():
    simulator.run()
    return "Hello"

@app.route('/getBodies')
def getBodies():
    print('getbodies')
    # simulator.update_info()

if __name__ == "__main__":
    app.run()
