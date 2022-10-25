#!/usr/bin/python3
"""places_amenities.py for API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask import make_response, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


# Retrieves the list of all Amenity objects of
# a Place: GET /api/v1/places/<place_id>/amenities
@app_views.route("/places/<string:place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def return_place_amenities(place_id):
    """return list of amenities of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    # check the storage type and retrieve the objects
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    for amenity in place_amenities:
        # to_dict() to retrieve an object into a valid JSON
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


# Deletes a Amenity object to a Place:
# DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """delete a amenity object to a place"""
    # get the place and the amenity
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    # get amenities of the place based on storage type
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return make_response(jsonify({}), 200)


# Link a Amenity object to a Place:
# POST /api/v1/places/<place_id>/amenities/<amenity_id>
@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """link an amenity to a place"""
    # get the amenity and the place
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    # get amenities of the place based on storage type
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenityto_dict()), 201)
