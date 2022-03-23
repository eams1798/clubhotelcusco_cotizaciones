#!/usr/bin/python3
"""This module controlls all the api resources"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    apiHost = getenv("HC_HOST", default="0.0.0.0")
    apiPort = getenv("HC_PORT", default=5000)
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host=apiHost, port=int(apiPort))
