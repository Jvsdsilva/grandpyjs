from flask import Flask, render_template, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from .model import parse
import requests
import json

# sys.path.append('..')

app = Flask(__name__)
Bootstrap(app)

# Initialize the extension
GoogleMaps(app)


@app.route('/')
def index():
    return render_template('base.html')


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    return response


def get_json():
    # Get the JSON.
    if request.method == "POST":
        data = request.get_json()

    return data


@app.route('/get_word', methods=['GET', 'POST'])
def get_history():
    # Get coordinates
    data = get_json()
    app_json = json.dumps(data)
    parser = parse.get_coordinates(app_json)
    history = parse.message(parser)

    # return summary to view html
    return jsonify({'html': history})


if __name__ == "__main__":
    app.run()
