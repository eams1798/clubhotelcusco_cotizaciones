#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base
from models.persona import Persona
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Persona(BaseModel, Base):
    """Estos atributos estarán compartidos por las clases Usuario y Cliente"""
    nombre = Column(String(128), nullable=False)
    apellido = Column(String(128), nullable=False)
    dni = Column(Integer, nullable=False)
    direccion = Column(String(256), nullable=False)
    telefono = Column(Integer, nullable=False)
    email = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """inicializa el cliente"""
        super().__init__(*args, **kwargs)
