from flask import jsonify

from ylio import app


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/shorten', methods=['POST'])
def shorten():
    return jsonify(greeting='hello world')


@app.route('/<id>')
def shortened(id):
    return 'not implemented yet'
