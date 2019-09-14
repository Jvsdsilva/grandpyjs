from flask import Flask, render_template, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from mediawiki import MediaWiki
from stop_words import get_stop_words, safe_get_stop_words
import requests
import json
import os


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


def get_json(url):
    """Takes a URL, and returns the JSON."""
    data = requests.get(url)

    return data.json()


@app.route('/get_word', methods=['GET', 'POST'])
def get_history():
    wikipedia = MediaWiki()
    # Get Ajax coordinates
    if request.method == "POST":
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        address = data['address']
    # sent coordinates to Media wiki
    query = wikipedia.geosearch(str(latitude), str(longitude))

    # Save first answer
    history = query[0]

    # sent answer to Media wiki
    summary = wikipedia.summary(history)

    answer = "Of course! There she is : " + address +\
             ". But have I already told you his story: " + summary
    # return summary to view html
    return jsonify({'html': answer})


if __name__ == "__main__":
    app.run()
