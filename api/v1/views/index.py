#!/usr/bin/python3
"""index.py for API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/status", strict_slashes=False)
def returnStatus():
    """return Status"""
    return jsonify({"status": "OK"})


# endpoint to retrieve the number of each objects by type
@app_views.route("/stats", strict_slashes=False)
def returnStats():
    """return stats"""
    dict_counts = {}
    for key, value in classes.items():
        dict_counts[key] = storage.count(value)
    return jsonify(dict_counts)
