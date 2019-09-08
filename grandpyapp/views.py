from flask import Flask, render_template, url_for, request, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from mediawiki import MediaWiki
from stop_words import get_stop_words, safe_get_stop_words
import requests
import json
import os


app = Flask(__name__)

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


@app.route('/get_word', methods=['GET', 'POST'])
def get_prediction():
    wikipedia = MediaWiki()
    if request.method == "POST":
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']

    # sent coordinates to Media wiki
    query = wikipedia.geosearch(str(latitude), str(longitude))

    # Save first answer
    history = query[0]

    # sent answer to Media wiki
    summary = wikipedia.summary(history)

    # return summary to view html
    return jsonify({'html': summary})


if __name__ == "__main__":
    app.run()
