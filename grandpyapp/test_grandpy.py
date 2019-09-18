import grandpyapp.model.parse as script
import grandpyapp.views as view
# content of test_show_warnings.py
import pytest
from mediawiki import MediaWiki
import requests
import json
import urllib.request


# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {
            "latitude": "48.8737917",
            "longitude": "2.2950275",
            "address": "Place Charles de Gaulle, 75008 Paris, France"
            }


def get_history():
    latlng = []
    lat = "48.856614"
    lng = "2.3522219"
    address = "Rue de Rivoli, 75001 Paris, France"

    # add to list
    latlng.append(lat)
    latlng.append(lng)
    latlng.append(address)
    # convert list into json format
    location = json.dumps(latlng)

    summary = script.message(location)

    return(summary)


def test_get_json(monkeypatch):

    results = {
        "latitude": 48.8737917,
        "longitude": 2.2950275,
        "address": "Place Charles de Gaulle, 75008 Paris, France"
        }
    location = json.dumps(results)

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    result = script.get_coordinates(location)
    assert result[1] == result[1]


def test_message():
    assert get_history()
