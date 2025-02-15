#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from flask import abort
from flask import jsonify
from flask import request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Handle GET requests to "/amenities" to retrieve all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["GET"],
        strict_slashes=False
        )
def get_amenity(amenity_id):
    """
    Handle GET requests to "/amenities/<amenity_id>"
    to retrieve an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_amenity(amenity_id):
    """Handle DELETE requests to "/amenities/<amenity_id>"
    to delete an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """Handle POST requests to "/amenities" to create an Amenity"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["PUT"],
        strict_slashes=False
        )
def put_amenity(amenity_id):
    """
    Handle PUT requests tp "/amenities/<amenity_id>"
    to update an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
