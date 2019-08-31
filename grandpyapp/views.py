from flask import Flask, render_template, url_for, request, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from mediawiki import MediaWiki
from stop_words import get_stop_words, safe_get_stop_words
import requests
import urllib.request, urllib.parse, urllib.error
import json

app = Flask(__name__)
# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']
# Initialize the extension
GoogleMaps(app)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/get_word')
def get_prediction():
    wikipedia = MediaWiki()
    word = request.args.get('word')
    # Set stop words language
    stop_words = get_stop_words('en')
    stop_words = get_stop_words('english')

    # split query
    filtered_sentence = ""
    filtered_sentence = word.split()

    reponse = []

    for each in filtered_sentence:
        if each not in stop_words:
            reponse.append(each)

    string_query = ' '.join(reponse)

    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    address = string_query

    if len(address) < 1:
        return

    try:
        url = serviceurl + "key=" + app.config['KEY_API'] +\
              "&" + urllib.parse.urlencode({'address': address})

        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        js = json.loads(data)
    except:
        print('==== Failure URL ====')
        js = None

    if not js:
        if 'status' not in js:
            if js['status'] != 'OK':
                print('==== Failure To Retrieve ====')
                print(js)

    else:
        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]

    # sent coordinates to Media wiki
    query = wikipedia.geosearch(str(lat), str(lng))

    # Save first answer
    history = query[0]

    # sent answer to Media wiki
    summary = wikipedia.summary(history)

    # return summary to view html
    return jsonify({'html': summary})


@app.route('/get_coord')
def get_coordinates():
    latlng = []
    reponse = []
    word = request.args.get('word')
    # Set stop words language
    stop_words = get_stop_words('en')
    stop_words = get_stop_words('english')

    # split query
    filtered_sentence = ""
    filtered_sentence = word.split()

    for each in filtered_sentence:
        if each not in stop_words:
            reponse.append(each)

    string_query = ' '.join(reponse)

    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    address = string_query

    try:
        url = serviceurl + "key=" + app.config['KEY_API'] +\
              "&" + urllib.parse.urlencode({'address': address})

        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        js = json.loads(data)
    except:
        print('==== Failure URL ====')
        js = None

    if not js:
        if 'status' not in js:
            if js['status'] != 'OK':
                print('==== Failure To Retrieve ====')
    else:
        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]

    latlng.append(lat)
    latlng.append(lng)

    location = json.dumps(latlng)

    # Return new coordinates to reload map view html
    return jsonify({'html': location})


if __name__ == "__main__":
    app.run(debug=True)
