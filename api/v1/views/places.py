#!/usr/bin/python3
"""places.py for API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask import make_response, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User



# Retrieves the list of all Place objects of a 
# City: GET /api/v1/cities/<city_id>/places
@app_views.route("/cities/<string:city_id>/places",
                 methods=['GET'], strict_slashes=False)
def return_places(city_id):
    """return list of places of a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        # to_dict() to retrieve an object into a valid JSON
        places.append(place.to_dict())
    return jsonify(places)


# Retrieves a Place object. : GET /api/v1/places/<place_id>
@app_views.route("/places/<string:place_id>",
                 methods=['GET'], strict_slashes=False)
def return_place(place_id):
    """return a place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


# Deletes a Place object: DELETE /api/v1/places/<place_id>
@app_views.route("/places/<string:place_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Creates a Place: POST /api/v1/cities/<city_id>/places
@app_views.route("/cities/<string:city_id>/places",
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """create a place in a city"""
    # get the city where to add a place
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    # make sure prerequisites are met
    # request.get_json transforms the HTTP body request to a dictionary
    # request to a dictionary
    args_json = request.get_json()
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in args_json:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user = storage.get("User", args_json['user_id'])
    if user is None:
        abort(404)

    if 'name' not in args_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    # create a new place with keyword args
    args_json['city_id'] = city_id
    place = Place(**args_json)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


# Updates a Place object: PUT /api/v1/places/<place_id>
@app_views.route("/places/<string:place_id>",
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    # get the place to update
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    # request.get_json transforms the HTTP body request to a dictionary
    # HTTP body request is not valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        # update and ignore id, user_id, city_id, created_at, updated_at
        if key not in ['id', 'user_id', 'city_id','created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
