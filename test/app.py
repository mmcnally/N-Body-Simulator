from flask import Flask, jsonify, render_template, request
import simulator
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
