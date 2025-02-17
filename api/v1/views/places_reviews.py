#!/usr/bin/python3
"""View for Review objects that handles all default RESTFul API actions"""
from flask import abort
from flask import jsonify
from flask import request

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
        "/places/<place_id>/reviews",
        methods=["GET"],
        strict_slashes=False
        )
def all_place_reviews(place_id):
    """
    Handle GET requests to "/places/<place_id>/reviews"
    to retrieve all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route(
        "/reviews/<review_id>",
        methods=["GET"],
        strict_slashes=False
        )
def get_review(review_id):
    """
    Handle GET requests to "/reviews/<review_id>" to retrieve a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        "/reviews/<review_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_review(review_id):
    """
    Handle DELETE requests to "/reviews/<review_id>" to delete a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/places/<place_id>/reviews",
        methods=["POST"],
        strict_slashes=False
        )
def post_review(place_id):
    """
    Handle POST requests to "/places/<place_id>/reviews" to create a Review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")
    new_review = Review(place_id=place_id, **data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        methods=["PUT"],
        strict_slashes=False
        )
def put_review(review_id):
    """
    Handle PUT requests to "/reviews/<review_id>" to update a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
