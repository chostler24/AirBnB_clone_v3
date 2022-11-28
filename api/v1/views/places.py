#!/usr/bin/python3
"""
    new view for places in RESTFul API
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.places import Place
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def place_list(city_id):
    """retrieves list of place objects"""
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


@app_views.route('/places/<place_id>', methods=['GET'])
def place_get(place_id):
    """retrieves a place object"""
    place_get = storage.get(Place, place_id)
    if place_get is not None:
        return jsonify(place_get.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """deletes a place object"""
    place_get = storage.get(Place, place_id)
    if place_get is not None:
        storage.delete(place_get)
        storage.save()
        return make_response(
            jsonify({}), 200
        )
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_create(city_id):
    """creates a place object"""
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

@app_views.route('/places/<place_id>', methods=['PUT'])
def place_update(place_id):
    """updates a place object"""
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
