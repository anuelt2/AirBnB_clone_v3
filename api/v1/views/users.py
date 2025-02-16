#!/usr/bin/python3
"""View for User objects that handles all default RESTFul API actions"""
from flask import abort
from flask import jsonify
from flask import request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """Handle GET requests to "/users" to retrieve all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    Handle GET requests to "/users/<user_id>" to retrieve a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    Handle DELETE requests to "/users/<user_id>" to delete a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """Handle POST requests to "/users" to create a User"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """
    Handle PUT requests tp "/users/<user_id>"
    to update a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignored_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
