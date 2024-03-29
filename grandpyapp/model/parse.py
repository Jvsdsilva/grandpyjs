from flask import Flask, render_template, url_for, request, jsonify
from stop_words import get_stop_words, safe_get_stop_words
import urllib.request, urllib.parse, urllib.error
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from mediawiki import MediaWiki
import requests
import json
import os


def get_coordinates(word):
    latlng = []
    key = os.environ.get('KEY')
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
    address = word

    if len(address) < 1:
        return()
    try:
        # Url construction
        url = serviceurl + "key=" + key + "&"\
              + urllib.parse.urlencode({'address': address})
        uh = urllib.request.urlopen(url)
        # decode answer
        data = uh.read().decode()
        # load json
        js = json.loads(data)
    except:
        location = "Any results!! Try again, please."
        print('==== Failure URL ====')
        js = None
        return(location)

    if js['status'] == 500:
        location = "Any results!! Try again, please."
        return(location)

    if not js:
        if 'status' not in js:
            if js['status'] != 'OK':
                print('==== Failure To Retrieve ====')
                print(js)
    # get all the informations from json
    if js['status'] == 'OK':
        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        address = js["results"][0]["formatted_address"]
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
