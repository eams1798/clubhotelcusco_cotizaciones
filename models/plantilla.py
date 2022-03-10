#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import Base, BaseModel
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Plantilla(BaseModel, Base):
    """Representación de un cliente"""
    __tablename__ = 'plantilla'
    # completar

    def __init__(self, *args, **kwargs):
        """inicializa el producto"""
        super().__init__(*args, **kwargs)
