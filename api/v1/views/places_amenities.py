#!/usr/bin/python3
"""
View for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify

from api.v1.views import app_views
from models import storage_t
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route(
        "/places/<place_id>/amenities",
        methods=["GET"],
        strict_slashes=False
        )
def all_place_amenities(place_id):
    """
    Handle GET requests to "/places/<place_id>/amenities"
    to retrieve all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if storage_t == "db":
        amenities = place.amenities
    else:
        amenities = [
                storage.get(Amenity, amenity_id)
                for amenity_id in place.amenity_ids
                ]
    return jsonify([amenity.to_dict() for amenity in amenities if amenity])


@app_views.route(
        "/places/<place_id>/amenities/<amenity_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_place_amenity(place_id, amenity_id):
    """
    Handle DELETE requests to "/places/<place_id>/amenities/<amenity_id>"
    to delete an Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/places/<place_id>/amenities/<amenity_id>",
        methods=["POST"],
        strict_slashes=False
        )
def link_amenity_place(place_id, amenity_id):
    """
    Handle POST requests to "/places/<place_id>/amenities/<amenity_id>"
    to link Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
