#!/usr/bin/python3
"""
    new view for User objs in RESTFul API
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError


@app_views.route('/users', methods=['GET'])
def user_list():
    """retrieves list of user objects"""
    dict_user = storage.all(User)
    user_list = []
    for user_get in dict_user.values():
        user_list.append(user_get.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def user_get(user_id):
    """retrieves a user object"""
    user_get = storage.get(User, user_id)
    if user_get is not None:
        return jsonify(user_get.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    """deletes a city object"""
    user_get = storage.get(User, user_id)
    if user_get is not None:
        storage.delete(user_get)
        storage.save()
        return make_response(
            jsonify({}), 200
        )
    abort(404)


@app_views.route('/users', methods=['POST'])
def user_create():
    """creates a city object"""
    req = request.get_json()
    if req is not None:
        if 'email' in req.keys() and req['email'] is not None:
            new = User(**req)
            new.save()
            return make_response(jsonify(new.to_dict()), 201)
        if 'password' in req.keys() and req['password'] is not None:
            new = User(**req)
            new.save()
            return make_response(jsonify(new.to_dict()), 201)
        return make_response(jsonify({
            'error': 'Missing email'
            }), 400)
    return make_response(jsonify({
        "error": "Not a JSON"
        }), 400)


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_update(user_id):
    """updates a user object"""
    req = request.get_json()
    if req is not None:
        check_user = storage.get(User, user_id)
        if check_user is None:
            abort(404)
        for key, val in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(check_user, key, val)
        storage.save()
        return make_response(jsonify(check_user.to_dict()), 200)
    return make_response(jsonify({
        "error": "Not a JSON"
        }), 400)
