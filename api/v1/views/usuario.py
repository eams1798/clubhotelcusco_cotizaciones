#!/usr/bin/python3
"""vista de objetos de la clase Usuario que maneja todas las acciones predeterminadas de la API RESTFul"""
from models.usuario import Usuario
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
import hashlib
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


@app_views.route('/login_usuario', methods=['POST'],
                 strict_slashes=False)
def login_usuario():
    """Permite el acceso de un usuario a la plataforma"""
    if not request or not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    response = request.get_json()
    if "correo" not in response:
        return make_response(jsonify({"error": "Falta correo"}), 400)
    if "contrasenia" not in response:
        return make_response(jsonify({"error": "Falta contraseña"}), 400)
    usuarios = storage.all("Usuario")
    for usuario in usuarios.values(): # posibilidad de actualizar esto por un algoritmo de búsqueda con complejidad menor a O(n^2)
        if response["correo"] == usuario.correo:
            passwd = hashlib.md5()
            passwd.update(response["contrasenia"].encode("utf-8"))
            passwd = passwd.hexdigest()
            if passwd != usuario.contrasenia:
                return make_response(jsonify({"error": "Contraseña incorrecta"}), 401)
            return jsonify(usuario.to_dict()), 200
    return make_response(jsonify({"error": "Correo no registrado"}), 401)
