#!/usr/bin/python3
"""
    new view for City objs in RESTFul API
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError


@app_views.route('/amenities', methods=['GET'])
def am_list():
    """retrieves list of am objects"""
    return jsonify(
        [am.to_dict() for am in storage.all(Amenity).values()]
    )


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def am_get(amenity_id):
    """retrieves am object"""
    am_get = storage.get(Amenity, amenity_id)
    if am_get is not None:
        return jsonify(am_get.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def am_delete(amenity_id):
    """deletes am object"""
    am_get = storage.get(Amenity, amenity_id)
    if am_get is not None:
        storage.delete(am_get)
        storage.save()
        return make_response(
            jsonify({}), 200
        )
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def am_create():
    """creates am object"""
    req = request.get_json()
    if req is not None:
        if "name" in req.keys() and req["name"] is not None:
            new_am = Amenity(**req)
            new_am.save()
            return make_response(jsonify(
                new_am.to_dict()
            ), 201)
        return make_response(jsonify(
            {"error": "Missing name"}
        ), 400)
    return make_response(jsonify(
        {"error": "Not a JSON"}
    ), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def am_update(amenity_id):
    """updates a city object"""
    req = request.get_json()
    if req is not None:
        check_am = storage.get(Amenity, amenity_id)
        if check_am is None:
            abort(404)
        for key, val in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(check_am, key, val)
        storage.save()
        return make_response(jsonify(
            check_am.to_dict()
        ), 200)
    return make_response(jsonify(
        {"error": "Not a JSON"}
        ), 400)
