from flask import Flask
from .views import app
app = Flask(__name__)
app.add_url_rule('/get_word', view_func=views.get_prediction)
app.add_url_rule('/get_coord', view_func=views.coordinates)