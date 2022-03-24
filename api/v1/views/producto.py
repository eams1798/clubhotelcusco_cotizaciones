#!/usr/bin/python3
"""vista de objetos de la clase Producto que maneja todas las acciones predeterminadas de la API RESTFul"""
from models.producto import Producto
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
import collections
import pdb


@app_views.route('/cotizaciones/<cotizacion_id>/productos', methods=['GET'],
                 strict_slashes=False)
def cotizacion_productos(cotizacion_id):
    """usuario by id"""
    # pdb.set_trace()
    cotizacion = storage.get("Cotizacion", cotizacion_id)
    if cotizacion is not None:
        prod_cotizaciones = [producto.to_dict() for producto in cotizacion.productos]
        return jsonify(prod_cotizaciones), 200
    return abort(404)


@app_views.route('/productos', methods=['GET'], strict_slashes=False)
def productos():
    """return all productos"""
    productos = [producto.to_dict() for producto in storage.all("Producto").values()]
    return jsonify(productos)


@app_views.route('/productos/<producto_id>', methods=['GET'],
                 strict_slashes=False)
def get_producto(producto_id):
    """producto by id"""
    # pdb.set_trace()
    producto = storage.get("Producto", producto_id)
    if producto is not None:
        producto = producto.to_dict()
        return jsonify(producto), 200
    return abort(404)


@app_views.route('/productos/<producto_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_producto(producto_id):
    """Delete producto by id"""
    producto = storage.get("Producto", producto_id)
    if producto is not None:
        producto.delete()
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/productos', methods=['POST'],
                 strict_slashes=False)
def post_producto():
    """Create a object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    response = request.get_json()
    for atr in Producto.atributosObligatorios(Producto):
        if atr not in response.keys():
            return make_response(jsonify({"error": "Missing one or more parameters"}), 400)
    for atr in response.keys():
        if atr not in Producto.atributos(Producto):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    obj = Producto(**response)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/productos/<producto_id>', methods=['PUT'],
                 strict_slashes=False)
def put_producto(producto_id):
    """Update a producto"""
    producto = storage.get("Producto", producto_id)
    if producto is None:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    response = request.get_json()
    for atr in response.keys():
        if atr not in Producto.atributos(Producto):
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    updatestat = producto.update(**response)
    # pdb.set_trace()
    if updatestat == -1:
        return make_response(jsonify({"error": "Bad parameters"}), 400)
    return jsonify(producto.to_dict())

@app_views.route('/filtro_productos', methods=['POST'],
                 strict_slashes=False)
def filtro_productos():
    """filtra productos según lo pedido
    
    Sintaxis JSON:
    {'atributo1': [lista], 'atributo2': [lista], ...}
    
    todos los argumentos de cada una de las listas son inclusivas entre el atributo del producto,
    pero los atributos del producto son exclusivas entre sí"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    response = request.get_json()

    filtros = ["proveedor", "categoria", "tipounidad", "productoOservicio", "publicoObjetivo"]
    for filtro in response.keys():
        if filtro not in filtros or type(response.get(filtro)) is not list:
            return make_response(jsonify({"error": "Bad parameters"}), 400)
    
    filtroProds = []
    productos = [producto for producto in storage.all("Producto").values()]

    filtroProveedor = []
    filtroCategoria = []
    filtroTipoUnidad = []
    filtroPoS = []
    filtroPublicoObj = []

    if "proveedor" in response.keys():
        for producto in productos:
            if producto.proveedor in response['proveedor']:
                filtroProveedor.append(producto.id)
    if "categoria" in response.keys():
        for producto in productos:
            if producto.categoria in response['categoria']:
                filtroCategoria.append(producto.id)
    if "tipoUnidad" in response.keys():
        for producto in productos:
            if producto.tipoUnidad in response['tipoUnidad']:
                filtroTipoUnidad.append(producto.id)
    if "productoOservicio" in response.keys():
        for producto in productos:
            if producto.productoOservicio in response['productoOservicio']:
                filtroPoS.append(producto.id)
    if "publicoObjetivo" in response.keys():
        for producto in productos:
            if producto.publicoObjetivo in response['publicoObjetivo']:
                filtroPublicoObj.append(producto.id)

    filtroProds += filtroProveedor + filtroCategoria + filtroTipoUnidad + filtroPoS + filtroPublicoObj

    conteoFiltro = dict(collections.Counter(filtroProds))
    maxRepetido = max([value for value in conteoFiltro.values()])

    idFiltrados = []
    for idFilt, conteoId in conteoFiltro.items():
        if conteoId == maxRepetido:
            idFiltrados.append(idFilt)
    
    productosFiltrados = []
    for producto in productos:
        if producto.id in idFiltrados:
            productosFiltrados.append(producto.to_dict())
    return jsonify(productosFiltrados), 200
