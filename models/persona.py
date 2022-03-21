#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Persona(BaseModel):
    """Estos atributos estarán compartidos por las clases Usuario y Cliente"""
    nombre = Column(String(128), nullable=False)
    apellido = Column(String(128), nullable=False)
    dni = Column(Integer)
    direccion = Column(String(256))
    telefono = Column(Integer)


    def __init__(self, *args, **kwargs):
        """inicializa el cliente"""
        super().__init__(*args, **kwargs)
