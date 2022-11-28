#!/usr/bin/python3
"""
    new view for reviews in RESTFul API
"""
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def rev_list(place_id):
    """retrieves list of review objects"""
    pl_dict = storage.all(Place)
    revs_list = None
    for pl in pl_dict.values():
        if pl.id == place_id:
            revs_list = pl.reviews
    if revs_list is not None:
        return jsonify(
            [rev.to_dict() for rev in revs_list]
        )
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def rev_get(review_id):
    """retrieves a review object"""
    rev_get = storage.get(Review, review_id)
    if rev_get is not None:
        return jsonify(rev_get.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def rev_delete(review_id):
    """deletes a review object"""
    rev_get = storage.get(Review, review_id)
    if rev_get is not None:
        storage.delete(rev_get)
        storage.save()
        return make_response(
            jsonify({}), 200
        )
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def rev_create(place_id):
    """creates a review object"""
    try:
        req = request.get_json()
        if req is not None:
            if 'user_id' not in req.keys():
                return make_response(jsonify(
                    {"error": "Missing user_id"}
                ), 400)
            if 'text' in req.keys():
                req['place_id'] = place_id
                new_rev = Review(**req)
                new_rev.save()
                return make_response(jsonify(
                    new_rev.to_dict()
                ), 201)
            return make_response(jsonify(
                {'error': 'Missing text'}
            ), 400)
        return make_response(jsonify(
            {"error": "Not a JSON"}
        ), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def rev_update(review_id):
    """updates a review object"""
    req = request.get_json()
    if req is not None:
        rev_check = storage.get(Review, review_id)
        if rev_check is None:
            abort(404)
        for key, val in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(rev_check, key, val)
        storage.save()
        return make_response(jsonify(
            rev_check.to_dict()
        ), 200)
    return make_response(jsonify(
        {"error": "Not a JSON"}
    ), 400)
