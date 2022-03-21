#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base, BaseModel
import sqlalchemy
from sqlalchemy import Column, String, BigInteger
# from sqlalchemy.orm import relationship
import pdb


class Proveedor(BaseModel, Base):
    """Representación de un cliente"""
    __tablename__ = 'proveedor'
    nombreEmpresa = Column(String(128), nullable=False)
    ruc = Column(BigInteger)
    nombreContacto = Column(String(128))
    direccion =  Column(String(128))
    telefono = Column(BigInteger)
    # productos = relationship("Producto", backref="cliente")

    def __init__(self, *args, **kwargs):
        """inicializa el proveedor"""
        # pdb.set_trace()
        super().__init__(*args, **kwargs)
