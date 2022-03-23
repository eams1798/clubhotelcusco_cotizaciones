#!/usr/bin/python3
"""vista de objetos de la clase Usuario que maneja todas las acciones predeterminadas de la API RESTFul"""
from models.usuario import Usuario
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
import pdb


@app_views.route('/usuarios', methods=['GET'], strict_slashes=False)
def usuarios():
    """return all usuarios"""
    usuarios = [usuario.to_dict() for usuario in storage.all("Usuario").values()]
    return jsonify(usuarios)


@app_views.route('/usuarios/<usuario_id>', methods=['GET'],
                 strict_slashes=False)
def get_usuario(usuario_id):
    """usuario by id"""
    # pdb.set_trace()
    usuario = storage.get("Usuario", usuario_id)
    if usuario is not None:
        usuario = usuario.to_dict()
        return jsonify(usuario), 200
    return abort(404)


@app_views.route('/usuarios/<usuario_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_usuario(usuario_id):
    """Delete usuario by id"""
    usuario = storage.get("Usuario", usuario_id)
    if usuario is not None:
        usuario.delete()
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/usuarios', methods=['POST'],
                 strict_slashes=False)
def post_usuario():
    """Create a object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    response = request.get_json()
    for atr in Usuario.atributosObligatorios(Usuario):
        if atr not in response.keys():
            return make_response(jsonify({"error": "Missing one or more parameters"}), 400)
    for atr in response.keys():
        if atr not in Usuario.atributos(Usuario):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    obj = Usuario(**response)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/usuarios/<usuario_id>', methods=['PUT'],
                 strict_slashes=False)
def put_usuario(usuario_id):
    """Update a usuario"""
    usuario = storage.get("Usuario", usuario_id)
    if usuario is None:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    response = request.get_json()
    for atr in response.keys():
        if atr not in Usuario.atributos(Usuario):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    updatestat = usuario.update(**response)
    # pdb.set_trace()
    if updatestat == -1:
        return make_response(jsonify({"error": "Bad parameters"}), 400)
    return jsonify(usuario.to_dict())
