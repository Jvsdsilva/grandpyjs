from flask import Flask, render_template, url_for, request, jsonify
from flask_googlemaps import GoogleMaps
from flask_bootstrap import Bootstrap
from flask_googlemaps import Map
from .model import parse
import requests
import json

app = Flask(__name__)
Bootstrap(app)
# Initialize the extension
GoogleMaps(app)
apikey = app.config['KEY_API']

@app.route('/')
def index():
    return render_template('base.html')


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    return response


@app.route('/get_word', methods=['GET', 'POST'])
def get_prediction():
    word = request.args.get('word')
    parser = parse.get_coordinates(word, apikey)
    history = parse.message(parser)

    # return history to view html
    return jsonify({'html': history})


@app.route('/get_coord', methods=['GET', 'POST'])
def get_coordinates():
    word = request.args.get('word')
    coordinates = parse.get_coordinates(word, apikey)

    # Return new coordinates to reload map view html
    return jsonify({'html': coordinates})


if __name__ == "__main__":
    app.run()
