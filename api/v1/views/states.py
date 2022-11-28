#!/usr/bin/python3
"""
    new view for State objs in RESTFul API
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states/', methods=['GET'])
def state_list():
    """list all state objects"""
    return jsonify([
        state.to_dict() for state in storage.all(State).values()
    ])


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """retrieves state object"""
    if state_id is not None:
        return jsonify([
            storage.get(State, state_id).to_dict()
        ])
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """deletes a state object"""
    if state_id is not None:
        storage.delete(storage.get(State, state_id))
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/', methods=['POST'])
def state_create():
    """creates a State"""
    if request.json():
        json_req = request.get_json(silent=True)
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


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_update(state_id):
    """updates state object"""
    loc = storage.get(State, state_id)
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
