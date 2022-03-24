#!/usr/bin/python3
"""Using blueprint"""
from flask import Blueprint


app_views = Blueprint(
    'app_views',
    __name__,
    url_prefix='/api/v1'
)


from api.v1.views.index import *
from api.v1.views.usuario import *
from api.v1.views.cliente import *
from api.v1.views.cotizacion import *
from api.v1.views.producto import *
""" *

from api.v1.views.producto_cotizacion import *"""
