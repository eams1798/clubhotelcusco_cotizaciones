#!/usr/bin/python3
""" holds class User"""
from datetime import datetime
import models
from models.base_model import Base, BaseModel, producto_cotizacion, time
import sqlalchemy
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
import json



class Cotizacion(BaseModel, Base):
    """Representación de un cliente"""
    __tablename__ = 'cotizacion'
    clienteId = Column(String(60), ForeignKey('cliente.id'), nullable=False)

    numAdultos = Column(Integer, nullable=False)
    numJovenes = Column(Integer, nullable=False)
    numNinos = Column(Integer, nullable=False)
    fechaEvento = Column(DateTime, nullable=False)
    tipoEvento = Column(String(128), nullable=False)
    estadoSolicitud = Column(String(50), nullable=False)

    productos = relationship("Cotizacion", secondary=producto_cotizacion,
                                        back_populates="cotizaciones")

    descuento = Column(Float, nullable=True)
    cantidadProductos = Column(Text, nullable=False)


    def __init__(self, *args, **kwargs):
        """inicializa el producto
        para el atriubuto cantidadProductos, se pasará un diccionario en str
        que contiene la cantidad de productos requeridos"""
        kw = kwargs.copy()
        if type(kw['cantProductos']) is not dict:
            return None
        del kw['cantProductos']
        super().__init__(*args, **kw)
        dictCantProductos = {}
        for producto in self.productos:
            """
            Ejemplo:
            dictCantProductos['id-bocadito01'] = 25
            dictCantProductos['id-bebida01'] = 75
            dictCantProductos['id-bocadito02'] = 44

            al pasarlo a diccionario:
            kw['productos'] = {'id-bocadito01': 25, 'id-bebida01': 75, 'id-bocadito02': 44}
            """
            dictCantProductos[getattr(producto, id)] = kwargs['cantProductos'][getattr(producto, id)] 
        kw['productos'] = json.dumps(**dictCantProductos)
        self.cantidadProductos = kw['productos']
        self.fechaEvento = datetime.strptime(kwargs["fechaEvento"], time)


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
        return total * self.descuento


    def totalComensales(self):
        return self.numAdultos + self.numJovenes + self.numNinos


    def cambiarEstadoSolicitud(self, nuevoEstado):
        self.estadoSolicitud = nuevoEstado
