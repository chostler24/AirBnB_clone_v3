#!/usr/bin/python3
"""Flask initialization"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """calls close method from storage"""
    storage.close()


if __name__ == "__main__":
    HOST = environ.get('HBNB_API_HOST', '0.0.0.0')
    PORT = environ.get('HBNB_API_PORT', '5000')
    app.run(host=HOST, port=PORT, threaded=True)
