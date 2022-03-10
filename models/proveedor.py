#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base, BaseModel
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Proveedor(BaseModel, Base):
    """Representación de un cliente"""
    __tablename__ = 'proveedor'
    nombreEmpresa = Column(String(128), nullable=False)
    ruc = Column(Integer, nullable=False)
    nombreContacto = Column(String(128), nullable=False)
    direccion =  Column(String(128), nullable=False)
    telefono = Column(Integer, nullable=False)
    productos = relationship("Producto", backref="cliente")

    def __init__(self, *args, **kwargs):
        """inicializa el proveedor"""
        super().__init__(*args, **kwargs)
