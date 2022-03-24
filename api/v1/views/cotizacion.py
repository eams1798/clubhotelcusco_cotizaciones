#!/usr/bin/python3
"""vista de objetos de la clase Cotizacion que maneja todas las acciones predeterminadas de la API RESTFul"""
from models.cotizacion import Cotizacion
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
import json
import pdb


@app_views.route('/clientes/<cliente_id>/cotizaciones', methods=['GET'], strict_slashes=False)
def cliente_cotizaciones(cliente_id):
    """muestra todas las cotizaciones de un cliente"""
    cliente = storage.get("Cliente", cliente_id)
    if cliente is not None:
        cot_cliente = [cotizacion.to_dict() for cotizacion in cliente.cotizaciones]
        print(cot_cliente)
        return jsonify(cot_cliente), 200
    return abort(404)


@app_views.route('/productos/<producto_id>/cotizaciones', methods=['GET'], strict_slashes=False)
def producto_cotizaciones(producto_id):
    """muestra todas las cotizaciones asociadas a un producto """
    producto = storage.get("Producto", producto_id)
    if producto is not None:
        cot_producto = [cotizacion.to_dict() for cotizacion in producto.cotizaciones]
        return jsonify(cot_producto), 200
    return abort(404)


@app_views.route('/cotizaciones', methods=['GET'], strict_slashes=False)
def cotizaciones():
    """return all cotizaciones"""
    cotizaciones = [cotizacion.to_dict() for cotizacion in storage.all("Cotizacion").values()]
    return jsonify(cotizaciones)


@app_views.route('/cotizaciones/<cotizacion_id>', methods=['GET'],
                 strict_slashes=False)
def get_cotizacion(cotizacion_id):
    """cotizacion by id"""
    # pdb.set_trace()
    cotizacion = storage.get("Cotizacion", cotizacion_id)
    if cotizacion is not None:
        cotizacion = cotizacion.to_dict()
        return jsonify(cotizacion), 200
    return abort(404)


@app_views.route('/cotizaciones/<cotizacion_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cotizacion(cotizacion_id):
    """Delete cotizacion by id"""
    cotizacion = storage.get("Cotizacion", cotizacion_id)
    if cotizacion is not None:
        cotizacion.delete()
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/cotizaciones', methods=['POST'],
                 strict_slashes=False)
def post_cotizacion():
    """Create a object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    response = request.get_json()
    for atr in Cotizacion.atributosObligatorios(Cotizacion):
        if atr not in response.keys():
            return make_response(jsonify({"error": "Missing one or more parameters"}), 400)
    for atr in response.keys():
        if atr not in Cotizacion.atributos(Cotizacion):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    obj = Cotizacion(**response)
    obj.save()
    dictobj = obj.to_dict()
    del dictobj['productos']
    return jsonify(dictobj), 201


@app_views.route('/cotizaciones/<cotizacion_id>', methods=['PUT'],
                 strict_slashes=False)
def put_cotizacion(cotizacion_id):
    """Update a cotizacion"""
    cotizacion = storage.get("Cotizacion", cotizacion_id)
    if cotizacion is None:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    response = request.get_json()
    for atr in response.keys():
        if atr not in Cotizacion.atributos(Cotizacion):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    updatestat = cotizacion.update(**response)
    # pdb.set_trace()
    if updatestat == -1:
        return make_response(jsonify({"error": "Bad parameters"}), 400)
    return jsonify(cotizacion.to_dict())
