#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base, BaseModel, producto_cotizacion
import sqlalchemy
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Producto(BaseModel, Base):
    """Representación de un cliente"""
    __tablename__ = 'producto'
    codigo = Column(String(16), nullable=False)
    nombre = Column(String(128), nullable=False)
    proveedor = Column(String(128), default="No especificado")
    precioPorUnidad = Column(Float, default=0)
    tipoUnidad = Column(String(20), nullable=False) # kg, platos, copas, ...
    capacidadPorUnidad = Column(Float, default=0) # ¿para cuántas personas es cada unidad de medida del producto?
    publicoObjetivo = Column(String(20), nullable=False) # adultos, jovenes o niños
    productoOservicio = Column(String(10), nullable=False)
    categoria = Column(String(32), nullable=False) # producto -> bebidas, entremeses, entradas, ...
                                                   # servicio -> reserva de espacios, música, personal externo, ...
    descripcion1 = Column(String(512)) # descripción para los usuarios de la plataforma
    descripcion2 = Column(String(512)) # descripción para los clientes
    enStock = Column(Float, default=0) # unidades en stock
    enOrden = Column(Float, default=0) # unidades en orden

    # proveedorId = Column(String(60), ForeignKey('proveedor.id'), nullable=False)

    cotizaciones = relationship("Cotizacion", secondary=producto_cotizacion,
                                        back_populates="productos")
    
    __atributosObligatorios = ["codigo", "nombre", "tipoUnidad", "publicoObjetivo", "productoOservicio", "categoria"]
    __atributos = __atributosObligatorios + ["proveedor", "precioPorUnidad", "capacidadPorUnidad",
                                             "descripcion1", "descripcion2", "enStock", "enOrden"]


    def __init__(self, *args, **kwargs):
        """inicializa el producto"""
        super().__init__(*args, **kwargs)


    def atributosObligatorios(self):
        return self.__atributosObligatorios


    def atributos(self):
        return self.__atributos
