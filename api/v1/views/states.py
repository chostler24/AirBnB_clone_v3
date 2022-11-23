#!/usr/bin/python3
"""
    new view for State objs in RESTFul API
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states/', methods=['GET'])
def states_stop():
    return jsonify([
        state.to_dict() for state in storage.all(State).values()
    ])


@app_views.route(
    '/states', methods=[
        'GET', 'DELETE', 'POST', 'PUT'
    ]
)
def states_slash(state_id=None):
    """handles state routing if given specific state"""
    req = flask.request.method
    loc = storage.get(State, state_id)
    if loc is None:
        abort(404)
    if req == 'GET':
        return jsonify(loc.to_dict())
    if req == 'DELETE':
        storage.delete(loc)
        storage.save()
        return make_response(jsonify({}), 200)
    if req == 'POST':
        if request.json():
            json_req = request.json()
            if "name" in json_req:
                new = State(**json_req)
                new.save()
                return make_response(
                    jsonify(new.to_dict()), 201
                )
            return make_response(
                jsonify({
                    "error": "Missing name"
                }), 400
            )
        return make_response(
            jsonify({
                "error": "Not a JSON"
            }), 400
        )
    if req == 'PUT':
        if request.get_json():
            for k, v in request.get_json().items():
                if k not in ("id", "created_at", "updated_at"):
                    loc[k] = v
            storage.save()
            return make_response(
                jsonify(loc.to_dict()), 400
            )
        return make_response(
            jsonify({
                "error": "Not a JSON"
            }), 400
        )
