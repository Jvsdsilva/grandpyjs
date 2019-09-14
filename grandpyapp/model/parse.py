from flask import Flask, render_template, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from stop_words import get_stop_words, safe_get_stop_words
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from mediawiki import MediaWiki
import requests
import json


def get_coordinates(query):
    latlng = []
    print(query)
    js = json.loads(query)

    print(js)

    lat = js["latitude"]
    lng = js["longitude"]
    address = js["address"]

    latlng.append(lat)
    latlng.append(lng)
    latlng.append(address)

    location = json.dumps(latlng)

    return(location)


def message(coordinates):
    data = json.loads(coordinates)

    latitude = data["latitude"]
    longitude = data["longitude"]
    address = data['address']

    wikipedia = MediaWiki()

    # sent coordinates to Media wiki
    query = wikipedia.geosearch(str(latitude), str(longitude))

    # Save first answer
    history = query[0]

    # sent answer to Media wiki
    summary = wikipedia.summary(history)

    answer = "Of course! There she is : " + address +\
             ". But have I already told you his story: " + summary
    return (answer)
