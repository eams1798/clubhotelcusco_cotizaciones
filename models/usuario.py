#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base
from models.persona import Persona
import sqlalchemy
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
import hashlib


class Usuario(Persona, Base):
    """Representación de un usuario de la plataforma"""
    __tablename__ = 'usuario'
    correo = Column(String(128), nullable=False)
    contrasenia = Column(String(128), nullable=False)
    rol = Column(String(128), nullable=False)
    estado = Column(String(32), nullable=False)
    loggedIn = Column(Boolean, default=False)

    __atributosObligatorios = ["nombre", "apellido", "correo", "contrasenia", "rol", "estado"]
    __atributos = __atributosObligatorios + ["dni", "direccion", "telefono"]


    def definirContrasena(self, _contrasenia):
        """encripta la contraseña pasada y la guarda en la instancia del
        usuario actual"""
        encrypt = hashlib.md5()
        encrypt.update(_contrasenia.encode("utf-8"))
        encrypt = encrypt.hexdigest()
        setattr(self, "contrasenia", encrypt)


    def __init__(self, *args, **kwargs):
        """inicializa el usuario"""
        if type(kwargs.get('contrasenia')) is str:
            clave = kwargs['contrasenia']
            del kwargs['contrasenia']
            super().__init__(*args, **kwargs)
            self.definirContrasena(clave)
        else:
            return None

    def update(self, **kwargs):
        if kwargs.get('contrasenia') is not None:
            _passwd = kwargs.get('contrasenia')
            del kwargs['contrasenia']
            self.definirContrasena(_passwd)
        super().update(**kwargs)


    def atributosObligatorios(self):
        return self.__atributosObligatorios


    def atributos(self):
        return self.__atributos
