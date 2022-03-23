#!/usr/bin/python3
"""object app_views that returns a JSON: status: OK"""
from flask import jsonify
from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status ok"""
    return jsonify({'status': 'ok'})


@app_views.route('/conteo', strict_slashes=False)
def count():
    """Return count"""
    return jsonify({
        "clientes": storage.count("Cliente"),
        "cotizaciones": storage.count("Cotizacion"),
        "productos": storage.count("Producto"),
        "usuarios": storage.count("Usuario"),
    })
