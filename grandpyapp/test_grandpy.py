import grandpyapp.views as script
# content of test_show_warnings.py
import pytest
from mediawiki import MediaWiki
import requests
import json

# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}

def get_history():
    wikipedia = script.MediaWiki()

    # sent coordinates to Media wiki
    query = wikipedia.geosearch("48.856614", "2.3522219")
 
    # Save first answer
    history = query[0]

    # sent answer to Media wiki
    summary = wikipedia.summary(history)
    return(summary)

def test_get_json(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # app.get_json, which contains requests.get, uses the monkeypatch
    result = script.get_json("https://fakeurl")
    assert result["mock_key"] == "mock_response"

def test_message():
    assert get_history()
