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
def rev_list():
    """retrieves list of review objects"""
    cit_dict = storage.all(City)
    pl_list = None
    for cit in cit_dict.values():
        if cit.id == city_id:
            pl_list = cit.places
    if pl_list is not None:
        return jsonify(
            [pl.to_dict() for pl in pl_list]
        )
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def rev_get():
    """retrieves a review object"""
    place_get = storage.get(Place, place_id)
    if place_get is not None:
        return jsonify(place_get.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def rev_delete():
    """deletes a review object"""
    place_get = storage.get(Place, place_id)
    if place_get is not None:
        storage.delete(place_get)
        storage.save()
        return make_response(
            jsonify({}), 200
        )
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def rev_create():
    """creates a review object"""
    try:
        req = request.get_json()
        if req is not None:
            if 'user_id' not in req.keys():
                return make_response(jsonify(
                    {"error": "Missing user_id"}
                ), 400)
            if 'name' in req.keys():
                req['city_id'] = city_id
                new_place = Place(**req)
                new_place.save()
                return make_response(jsonify(
                    new_place.to_dict()
                ), 201)
            return make_response(jsonify(
                {'error': 'Missing name'}
            ), 400)
        return make_response(jsonify(
            {"error": "Not a JSON"}
        ), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def rev_update():
    """updates a review object"""
    req = request.get_json()
    if req is not None:
        check_place = storage.get(Place, place_id)
        if check_place is None:
            abort(404)
        for key, val in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(check_place, key, val)
        storage.save()
        return make_response(jsonify(
            check_place.to_dict()
        ), 200)
    return make_response(jsonify(
        {"error": "Not a JSON"}
    ), 400)
