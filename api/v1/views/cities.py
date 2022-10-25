#!/usr/bin/python3
"""cities.py for API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask import make_response, abort, request
from models import storage
from models.state import State
from models.state import City


# Retrieves the list of all City objects of a
# State: GET /api/v1/states/<state_id>/cities
@app_views.route("/states/<string:state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def return_cities(state_id):
    """return list of cities of a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        # to_dict() to retrieve an object into a valid JSON
        cities.append(city.to_dict())
    return jsonify(cities)


# Retrieves a City object. : GET /api/v1/cities/<city_id>
@app_views.route("/cities/<string:city_id>",
                 methods=['GET'], strict_slashes=False)
def return_city(city_id):
    """return a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


# Deletes a City object: DELETE /api/v1/cities/<city_id>
@app_views.route("/cities/<string:city_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Creates a City: POST /api/v1/states/<state_id>/cities
@app_views.route("/states/<string:state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """create a city in a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    # make sure prerequisites are met
    # request.get_json transforms the HTTP body request to a dictionary
    # request to a dictionary
    if not request.get_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    # create a new city with the appropriate state id
    args_json = request.get_json()
    args_json['state_id'] = state_id
    city = City(**args_json)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


# Updates a City object: PUT /api/v1/cities/<city_id>
@app_views.route("/cities/<string:city_id>",
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a state"""
    # get the city to update
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    # request.get_json transforms the HTTP body request to a dictionary
    # HTTP body request is not valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        # update and ignore id,state_id, created_at, updated_at
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
