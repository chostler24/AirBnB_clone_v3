#!/usr/bin/python3
"""
    new view for State objs in RESTFul API
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify


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
def states_slash():
    pass
