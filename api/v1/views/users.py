#!/usr/bin/python3
"""cities.py for API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask import make_response, abort, request
from models import storage
from models.user import User


# Retrieves the list of all User objects: GET /api/v1/users
@app_views.route("/users",
                 methods=['GET'], strict_slashes=False)
def return_users(state_id):
    """return list of users"""
    users = []
    for user in storage.all("User").values:
        # to_dict() to retrieve an object into a valid JSON
        users.append(user.to_dict())
    return jsonify(users)


# Retrieves a User object: GET /api/v1/users/<user_id>
@app_views.route("/users/<string:user_id>",
                 methods=['GET'], strict_slashes=False)
def return_user(user_id):
    """return a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# Deletes a User object:: DELETE /api/v1/users/<user_id>
@app_views.route("/users/<string:user_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Creates a User: POST /api/v1/users
@app_views.route("/users",
                 methods=['POST'], strict_slashes=False)
def create_user(state_id):
    """create a user"""
    # make sure prerequisites are met
    # request.get_json transforms the HTTP body request to a dictionary
    # request to a dictionary
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    # create a new user
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


# Updates a User object: PUT /api/v1/users/<user_id>
@app_views.route("/users/<string:user_id>",
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    # get the user to update
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    # request.get_json transforms the HTTP body request to a dictionary
    # HTTP body request is not valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        # update and ignore id, email, created_at, updated_at
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
