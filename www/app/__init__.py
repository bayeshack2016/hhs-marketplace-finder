from flask import Flask
from flask.ext.googlemaps import GoogleMaps

app = Flask(__name__)
GoogleMaps(app)

from app import views
