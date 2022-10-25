#!/usr/bin/python3
"""amneties.py for API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask import make_response, abort, request
from models import storage
from models.amenity import Amenity


# Retrieves the list of all Amenity objects: GET /api/v1/amenities
@app_views.route("/amenities",
                 methods=['GET'], strict_slashes=False)
def return_amenities():
    """return list of amenities"""
    amenities = []
    for amenity in storage.all("Amenity").values:
        # to_dict() to retrieve an object into a valid JSON
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


# Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
@app_views.route("/amenities/<string:amenity_id>",
                 methods=['GET'], strict_slashes=False)
def return_amenity(amenity_id):
    """return a amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


# Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
@app_views.route("/amenities/<string:amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Creates a Amenity: POST /api/v1/amenities
@app_views.route("/amenities",
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a amenity"""
    # make sure prerequisites are met
    # request.get_json transforms the HTTP body request to a dictionary
    # request to a dictionary
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    # create a new amenity with json kwargs
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


# Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
@app_views.route("/amenities/<string:amenity_id>",
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update a amenity"""
    # get the amenity to update
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    # request.get_json transforms the HTTP body request to a dictionary
    # HTTP body request is not valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        # update and ignore id, created_at, updated_at
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
