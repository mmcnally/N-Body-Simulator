from flask import Flask
import simulator
app = Flask(__name__)

@app.route("/")
def hello():
    simulator.run()
    return "Hello"

if __name__ == "__main__":
    app.run()
