from flask import Flask, render_template, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from stop_words import get_stop_words, safe_get_stop_words
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from mediawiki import MediaWiki
import requests
import json


def get_coordinates(query):
    print(query)
    latlng = []

    js = json.loads(query)
    # get data from json
    lat = js["latitude"]
    lng = js["longitude"]
    address = js["address"]
    # add to list
    latlng.append(lat)
    latlng.append(lng)
    latlng.append(address)
    # convert list into json format
    location = json.dumps(latlng)

    # return location
    return(location)


def message(coordinates):
    data = json.loads(coordinates)
    # get data from json
    latitude = data[0]
    longitude = data[1]
    address = data[2]

    # instanciation wikipedia object
    wikipedia = MediaWiki()

    # sent coordinates to Media wiki
    query = wikipedia.geosearch(str(latitude), str(longitude))

    # Save first answer
    history = query[0]

    # sent answer to Media wiki
    summary = wikipedia.summary(history)

    # format answer to display
    answer = "Of course! There she is : " + address +\
             ". But have I already told you his history: " + summary
    return (answer)
