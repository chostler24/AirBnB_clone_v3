#!/usr/bin/python3
"""
    new view for State objs in RESTFul API
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'])
def state_list():
    """list all state objects"""
    return jsonify(
        [st.to_dict() for st in storage.all(State).values()]
    )


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """retrieves state object"""
    get_check = storage.get(State, state_id)
    if get_check is not None:
        return jsonify(
            get_check.to_dict()
        )
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """deletes a state object"""
    if state_id is not None:
        storage.delete(storage.get(State, state_id))
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'])
def state_create():
    """creates a State"""
    req = request.get_json()
    if req is not None:
        if 'name' in req.keys() and req['name'] is not None:
            new = State(**req)
            new.save()
            return make_response(jsonify(new.to_dict()), 201)
        return make_response(jsonify({
            'error': 'Missing name'
        }), 400)
    return make_response(jsonify({
        "error": "Not a JSON"
    }), 400)


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_update(state_id):
    """updates state object"""
    req = request.get_json()
    if req is not None:
        check_state = storage.get(State, state_id)
        if check_state is None:
            abort(404)
        for key, val in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(check_state, key, val)
        storage.save()
        return make_response(jsonify(check_state.to_dict()), 200)
    return make_response(jsonify({
        "error": "Not a JSON"
    }), 400)
