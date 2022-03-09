#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base
from models.persona import Persona
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import hashlib


class Usuario(Persona, Base):
    """Representación de un usuario de la plataforma"""
    __tablename__ = 'usuario'
    contrasena = Column(String(128), nullable=False)
    rango(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """inicializa el usuario"""
        super().__init__(*args, **kwargs)

    def definirContrasena(self, _contrasena):
        """encripta la contraseña pasada y la guarda en la instancia del
        usuario actual"""
        encrypt = hashlib.md5()
        encrypt.update(_contrasena.encode("utf-8"))
        encrypt = encrypt.hexdigest()
        setattr(self, "contrasena", encrypt)

