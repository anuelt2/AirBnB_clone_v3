#!/usr/bin/python3
"""Defines index route for Flask application"""
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def count():
    """Retrieves number of objects by type"""
    return jsonify(
            {
                "amenities": storage.count(Amenity),
                "cities": storage.count(City),
                "places": storage.count(Place),
                "reviews": storage.count(Review),
                "states": storage.count(State),
                "users": storage.count(User)
                }
            )
