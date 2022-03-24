#!/usr/bin/python3
"""vista de objetos de la clase Cliente que maneja todas las acciones predeterminadas de la API RESTFul"""
from models.cliente import Cliente
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
import pdb


@app_views.route('/clientes', methods=['GET'], strict_slashes=False)
def clientes():
    """return all clientes"""
    clientes = [cliente.to_dict() for cliente in storage.all("Cliente").values()]
    return jsonify(clientes)


@app_views.route('/clientes/<cliente_id>', methods=['GET'],
                 strict_slashes=False)
def get_cliente(cliente_id):
    """cliente by id"""
    # pdb.set_trace()
    cliente = storage.get("Cliente", cliente_id)
    if cliente is not None:
        cliente = cliente.to_dict()
        return jsonify(cliente), 200
    return abort(404)


@app_views.route('/clientes/<cliente_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cliente(cliente_id):
    """Delete cliente by id"""
    cliente = storage.get("Cliente", cliente_id)
    if cliente is not None:
        cliente.delete()
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/clientes', methods=['POST'],
                 strict_slashes=False)
def post_cliente():
    """Create a object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    response = request.get_json()
    for atr in Cliente.atributosObligatorios(Cliente):
        if atr not in response.keys():
            return make_response(jsonify({"error": "Missing one or more parameters"}), 400)
    for atr in response.keys():
        if atr not in Cliente.atributos(Cliente):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    obj = Cliente(**response)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/clientes/<cliente_id>', methods=['PUT'],
                 strict_slashes=False)
def put_cliente(cliente_id):
    """Update a cliente"""
    cliente = storage.get("Cliente", cliente_id)
    if cliente is None:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    response = request.get_json()
    for atr in response.keys():
        if atr not in Cliente.atributos(Cliente):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    updatestat = cliente.update(**response)
    # pdb.set_trace()
    if updatestat == -1:
        return make_response(jsonify({"error": "Bad parameters"}), 400)
    return jsonify(cliente.to_dict())
