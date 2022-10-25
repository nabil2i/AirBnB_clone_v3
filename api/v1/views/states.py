#!/usr/bin/python3
"""states.py for API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask import make_response, abort, request
from models import storage
from models.state import State


# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route("/states", methods=['GET'], strict_slashes=False)
def return_states():
    """return list of States"""
    states = []
    for state in storage.all("State").values():
        # to_dict() to retrieve an object into a valid JSON
        states.append(state.to_dict())
    return jsonify(states)


# Retrieves a State object: GET /api/v1/states/<state_id>
@app_views.route("/states/<string:state_id>",
                 methods=['GET'], strict_slashes=False)
def return_state(state_id):
    """return a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


# Deletes a State object:: DELETE /api/v1/states/<state_id>
@app_views.route("/states/<string:state_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Creates a State: POST /api/v1/states
@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """create a state"""
    # make sure prerequisites are met
    # request.get_json transforms the HTTP body request to a dictionary
    # request to a dictionary
    if not request.get_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    # create a new state with keyword args
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


# Updates a State object: PUT /api/v1/states/<state_id>
@app_views.route("/states/<string:state_id>",
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""
    # get the state to update
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    # request.get_json transforms the HTTP body request to a dictionary
    # HTTP body request is not valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        # update and ignore id, created_at, updated_at
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
