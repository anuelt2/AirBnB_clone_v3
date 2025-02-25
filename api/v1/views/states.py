#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from flask import abort
from flask import jsonify
from flask import request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
    Handle GET requests to "/states" to retrieve list of all State objects
    """
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """
    Handle GET requests to "/states/<state_id>" to retrieve a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        "/states/<state_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_state(state_id):
    """
    Handle DELETE requests to "/states/<state_id>" to delete a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """Handle POST requests to "/states" to create a State"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """Handle PUT requests to "/states/<state_id>" to update a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
