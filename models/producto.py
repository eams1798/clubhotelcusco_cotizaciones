#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base, BaseModel, producto_cotizacion
import sqlalchemy
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship


class Producto(BaseModel, Base):
    """Representación de un cliente"""
    __tablename__ = 'producto'
    nombre = Column(String(128), nullable=False)
    precioPorUnidad = Column(Float, nullable=True)
    capacidadPorUnidad = Column(Float, nullable=True)
    tipoUnidad = Column(String(20), nullable=False)
    publicoObjetivo = Column(String(20), nullable=False)
    categoría = Column(String(32), nullable=False)
    descripcion1 = Column(String(512), nullable=False)
    descripcion2 = Column(String(512), nullable=False)
    enStock = Column(Float, nullable=True)
    enOrden = Column(Float, nullable=True)

    proveedorId = Column(String(60), ForeignKey('proveedor.id'), nullable=False)

    cotizaciones = relationship("Cotizacion", secondary=producto_cotizacion,
                                        back_populates="productos")


    def __init__(self, *args, **kwargs):
        """inicializa el producto"""
        super().__init__(*args, **kwargs)
