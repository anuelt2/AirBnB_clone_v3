#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from flask import abort
from flask import jsonify
from flask import request

from api.v1.views import app_views
from models import storage
from models import storage_t
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route(
        "/cities/<city_id>/places",
        methods=["GET"],
        strict_slashes=False
        )
def all_city_places(city_id):
    """
    Handle GET requests to "/cities/<city_id>/places"
    to retrieve all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Handle GET requests to "/places/<place_id>" to retrieve a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        "/places/<place_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_place(place_id):
    """
    Handle DELETE requests to "/places/<place_id>" to delete a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/cities/<city_id>/places",
        methods=["POST"],
        strict_slashes=False
        )
def post_place(city_id):
    """Handle POST requests to "/cities/<city_id>/places" to create a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    new_place = Place(city_id=city_id, **data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """
    Handle PUT requests to "/places/<place_id>" to update a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Handle POST requests to "/places_search" to retrieve all Place objects
    depending on the JSON in the body of the request
    """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if data == {} or all(
            isinstance(value, list) and not value
            for value in data.values()):
        places = list(storage.all(Place).values())
        return jsonify([place.to_dict() for place in places])

    s_cities = []
    if data.get("states"):
        states = [storage.get(State, state_id)
                  for state_id in data["states"]
                  if storage.get(State, state_id)]
        s_cities = [city for state in states for city in state.cities]
        #places = [place for city in s_cities for place in city.places]

    cities = []
    if data.get("cities"):
        cities = [storage.get(City, city_id)
                  for city_id in data["cities"]
                  if storage.get(City, city_id)]
        #places = [place for city in cities for place in city.places]

    all_cities = set(s_cities + cities)
    places = [place for city in all_cities for place in city.places]

    if data.get("amenities"):
        #amenities = [storage.get(Amenity, amenity_id)
        #             for amenity_id in data["amenities"]
        #             if storage.get(Amenity, amenity_id)]

        amenities = []
        for amenity_id in data["amenities"]:
            amenity = storage.get(Amenity, amenity_id)
            amenity = amenity.to_dict()
            amenity_ids = amenity["id"]
            amenities.append(amenity_ids)

        if not places:
            places = list(storage.all(Place).values())

        #filtered_places = []
        #p_amen = []
        #for place in places:
        #    if storage_t == "db":
        #        place_amenities = place.amenities
        #    else:
        #        place_amenities = [storage.get(Amenity, amenity_id)
        #                           for amenity_id in place.amenities]
        #    place_amenities = place_amenities.to_dict()
        #    p_amen.append(place_amenities)

            #place_amenities = place_amenities
         #   if all(amenity in p_amen for amenity in amenities):
          #      filtered_places.append(place)

        #places = filtered_places
        return places

    return jsonify([place.to_dict() for place in places])
