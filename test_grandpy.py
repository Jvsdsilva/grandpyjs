import grandpyapp.views as script
# content of test_show_warnings.py
import warnings
from flask import Flask, render_template, url_for, request, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from mediawiki import MediaWiki
from stop_words import get_stop_words, safe_get_stop_words
import requests
import urllib.request, urllib.parse, urllib.error
import json
app = Flask(__name__)

def test_coordinates():
    latlng = []
    reponse = []
    word = "Do you know Paris"
    # Set stop words language
    stop_words = script.get_stop_words('en')
    stop_words = script.get_stop_words('english')

    # split query
    filtered_sentence = ""
    filtered_sentence = word.split()
    print (filtered_sentence)
    reponse = []

    for each in filtered_sentence:
        if each not in stop_words:
            reponse.append(each)

    string_query = ' '.join(reponse)

    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    address = string_query
    print (address)
    if len(address) < 1:
        return
    print (script.app.config['KEY_API'])
    
    try:
        url = serviceurl + "key=" + script.app.config['KEY_API'] +\
              "&" + script.urllib.parse.urlencode({'address': address})
        print (url)
        uh = script.urllib.request.urlopen(url)
        print (uh)
        data = uh.read().decode()
        print (data)
        js = script.json.loads(data)
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
    
    print(lat)
    print(lng)

    latlng.append(lat)
    latlng.append(lng)
    print(latlng)

    location = script.json.dumps(latlng)
    print(location)

def test_message():
    wikipedia = script.MediaWiki()
    print(wikipedia)
    # sent coordinates to Media wiki
    query = wikipedia.geosearch("48.856614", "2.3522219")
    print (query)
    # Save first answer
    history = query[0]
    print (history)
    # sent answer to Media wiki
    summary = wikipedia.summary(history)
    print (summary)

