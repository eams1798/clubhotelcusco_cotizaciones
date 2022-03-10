#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table, PrimaryKeyConstraint
import uuid


time = "%Y-%m-%d %H:%M:%S.%f"
Base = declarative_base()

producto_cotizacion = Table('producto_cotizacion',
                            Base.metadata,
                            Column('productoId', String(60), ForeignKey('producto.id'), nullable=False),
                            Column('cotizacionId', String(60), ForeignKey('cotizacion.id'), nullable=False),
                            PrimaryKeyConstraint('productoId', 'cotizacionId'))

class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id = Column(String(60), primary_key=True)
    creado = Column(DateTime, default=datetime.utcnow)
    actualizado = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("creado", None) and type(self.creado) is str:
                self.creado = datetime.strptime(kwargs["creado"], time)
            else:
                self.creado = datetime.utcnow()
            if kwargs.get("actualizado", None) and type(self.actualizado) is str:
                self.actualizado = datetime.strptime(kwargs["actualizado"], time)
            else:
                self.actualizado = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.creado = datetime.utcnow()
            self.actualizado = self.creado

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'actualizado' with the current datetime"""
        self.actualizado = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()
    
    def registrar(self):
        """registra la instancia en la base de datos. Es otro nombre para el
        método 'save'"""
        self.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "creado" in new_dict:
            new_dict["creado"] = new_dict["creado"].strftime(time)
        if "actualizado" in new_dict:
            new_dict["actualizado"] = new_dict["actualizado"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if hasattr(self, "contrasena"):
            del new_dict["contrasena"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
