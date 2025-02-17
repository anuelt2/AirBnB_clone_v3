#!/usr/bin/python3
"""View for City objects that handles all default RESTFul API actions"""
from flask import abort
from flask import jsonify
from flask import request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
        "/states/<state_id>/cities",
        methods=["GET"],
        strict_slashes=False
        )
def all_state_cities(state_id):
    """
    Handle GET requests to "/states/<state_id>/cities"
    to retrieve all City objects of a State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city(city_id):
    """Handle GET requests to "/cities/<city_id>" to retrieve a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Handle DELETE requests to "/city/<city_id>" to delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/states/<state_id>/cities",
        methods=["POST"],
        strict_slashes=False
        )
def post_city(state_id):
    """Handle POST requests to "/states/<state_id>/cities" to create a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    new_city = City(state_id=state_id, **data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """Handle PUT requests to "/cities/<city_id>" to update a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
