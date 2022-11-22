#!/usr/bin/python3
"""
    routes for our api and web server
"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def status():
    return jsonify(
        {"status":"OK"}
    )
