#!/usr/bin/python3
""" holds class User"""
from datetime import datetime
import models
from models.base_model import Base, BaseModel, producto_cotizacion, ftime
import sqlalchemy
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import json
import pdb



class Cotizacion(BaseModel, Base):
    """Representación de un cliente"""
    __tablename__ = 'cotizacion'
    clienteId = Column(String(60), ForeignKey('cliente.id'), nullable=False)

    numAdultos = Column(Integer, default=0)
    numJovenes = Column(Integer, default=0)
    numNinos = Column(Integer, default=0)
    fechaEvento = Column(DateTime, nullable=False)
    tipoEvento = Column(String(128), nullable=False)
    estadoSolicitud = Column(String(50), nullable=False)

    productos = relationship("Producto", secondary=producto_cotizacion,
                                        back_populates="cotizaciones")

    descuento = Column(Float, default=0)
    cantidadProductos = Column(Text, nullable=False)


    def actualizarProductos(self, string="", **cantProductos):
        if type(cantProductos) is dict:
            if cantProductos is {}:
                self.productos = []
            else:
                prods = models.storage.all("Producto")
                for prodId in cantProductos.keys():
                    if f"Producto.{prodId}" not in prods.keys():
                        return -1
                listaProductos = []
                for key in prods.keys():
                    if f'{key.split(".")[1]}' in cantProductos.keys():
                        listaProductos.append(prods[key])
                self.productos = listaProductos
            self.cantidadProductos = json.dumps(cantProductos)
            if string != "fromInit":
                super().update()
            return 0
        else:
            return -1


    def __init__(self, *args, **kwargs):
        """
        1. verificar si kwargs tiene un item llamado cantidadProductos (debe ser un diccionario)
        2. guardar kwargs['cantidadProductos'] en otra variable (listaProductos)
        3. borrar kwargs['cantidadProductos']
        4. super.__init__(...)
        5. listaProductos debe tener el siguiente formato: {'productoId': cantidad, ...}
        6. buscar en Productos si las id coinciden
        7. si todas coinciden, guardar las id de los productos en self.productos
        8. de lo anterior, guardar listaProductos en self.cantidadProductos en formato string
        """
        if type(kwargs.get('cantidadProductos')) is dict:
            cantProductos = kwargs['cantidadProductos']
            del kwargs['cantidadProductos']
            fechaEv = kwargs['fechaEvento']
            del kwargs['fechaEvento']
            super().__init__(**kwargs)
            # pdb.set_trace()
            if self.actualizarProductos("fromInit", **cantProductos) == -1:
                return None
            else:
                self.fechaEvento = datetime.strptime(fechaEv, ftime)
    
    def update(self, **kwargs):
        if kwargs is not None and type(kwargs.get('clienteId')) is None:
            if type(kwargs.get('cantidadProductos')) is dict:
                cantProductos = kwargs['cantidadProductos']
                del kwargs['cantidadProductos']
                if self.actualizarProductos(**cantProductos) == -1:
                    return None
            if type(kwargs.get('fechaEvento')) is str:
                fechaEv = kwargs['fechaEvento']
                del kwargs['fechaEvento']
                self.fechaEvento = datetime.strptime(fechaEv, ftime)
            super.update(**kwargs)


    def getCantidadProductos(self):
        return json.loads(self.cantidadProductos)


    def precioTotalProducto(self, producto_id):
        cantidad = getCantidadProductos().get(producto_id)
        if cantidad is not None:
            for producto in self.productos:
                if producto_id == getattr(producto, id):
                    return cantidad * getattr(producto, 'precioPorUnidad')
        return 0


    def precioTotal(self):
        total = 0
        cantidades = self.getCantidadProductos()
        for producto in productos:
            precio = getattr(producto, 'precioPorUnidad')
            cantidad = cantidades[getattr(producto, 'id')]
            total += (precio * cantidad)
        return total * (1 - self.descuento)


    def totalComensales(self):
        return self.numAdultos + self.numJovenes + self.numNinos


    def cambiarEstadoSolicitud(self, nuevoEstado):
        self.estadoSolicitud = nuevoEstado
