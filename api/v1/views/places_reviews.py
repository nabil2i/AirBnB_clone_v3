#!/usr/bin/python3
"""places_reviews.py for API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask import make_response, abort, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


# Retrieves the list of all Review objects of
# a Place: GET /api/v1/places/<place_id>/reviews
@app_views.route("/places/<string:place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def return_reviews(place_id):
    """return list of reveiws of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        # to_dict() to retrieve an object into a valid JSON
        reviews.append(review.to_dict())
    return jsonify(reviews)


# Retrieves a Review object. : GET /api/v1/reviews/<review_id>
@app_views.route("/reviews/<string:review_id>",
                 methods=['GET'], strict_slashes=False)
def return_review(review_id):
    """return a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


# Deletes a Review object: DELETE /api/v1/reviews/<review_id>
@app_views.route("/reviews/<string:review_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Creates a Review: POST /api/v1/places/<place_id>/reviews
@app_views.route("/places/<string:place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """create a review for a place"""
    # get the place where to add a review
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    # make sure prerequisites are met
    # request.get_json transforms the HTTP body request to a dictionary
    # request to a dictionary
    args_json = request.get_json()
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in args_json:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    # get the user who made the review
    user = storage.get("User", args_json['user_id'])
    if user is None:
        abort(404)

    if 'text' not in args_json:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    # create a new place with keyword args
    args_json['place_id'] = place_id
    review = Review(**args_json)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


# Updates a Review object: PUT /api/v1/reviews/<review_id>
@app_views.route("/reviews/<string:review_id>",
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review"""
    # get the review to update
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    # request.get_json transforms the HTTP body request to a dictionary
    # HTTP body request is not valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        # update and ignore id, user_id, place_id, created_at, updated_at
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
