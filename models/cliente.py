#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base
from models.persona import Persona
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import hashlib


class Cliente(Persona, Base):
    """Representación de un cliente"""
    __tablename__ = 'cliente'
    cotizaciones = relationship("Cotizacion", backref="cliente")

    def __init__(self, *args, **kwargs):
        """inicializa el cliente"""
        super().__init__(*args, **kwargs)
