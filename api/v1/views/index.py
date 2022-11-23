#!/usr/bin/python3
"""
    routes for our api and web server
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status')
def status():
    return jsonify(
        {"status": "OK"}
    )


@app_views.route('/api/v1/stats')
def stats():
    """creates endpoint that retrieves # of objs of given type"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    })
