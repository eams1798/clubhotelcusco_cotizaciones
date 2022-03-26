#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime, timezone
import models
import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table, PrimaryKeyConstraint
import json
import uuid


ftime = "%d-%m-%Y %H:%M:%S"
Base = declarative_base()

producto_cotizacion = Table('producto_cotizacion',
                            Base.metadata,
                            Column('productoId', String(60), ForeignKey('producto.id'), nullable=False),
                            Column('cotizacionId', String(60), ForeignKey('cotizacion.id'), nullable=False),
                            PrimaryKeyConstraint('productoId', 'cotizacionId'))


def utclocal():
    """Devuelve el momento actual en la hora local"""
    utcnow = datetime.utcnow()
    nowlocal = utcnow.replace(tzinfo=timezone.utc).astimezone(tz=None)
    localtime = datetime.strptime(nowlocal.strftime(ftime), ftime)
    return localtime


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id = Column(String(60), primary_key=True)
    creado = Column(DateTime, default=utclocal())
    actualizado = Column(DateTime, default=utclocal())

    __atributosObligatorios = []
    __atributos = []

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("creado", None) and type(self.creado) is str:
                self.creado = datetime.strptime(kwargs["creado"], ftime)
            else:
                self.creado = utclocal()
            if kwargs.get("actualizado", None) and type(self.actualizado) is str:
                self.actualizado = datetime.strptime(kwargs["actualizado"], ftime)
            else:
                self.actualizado = utclocal()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.creado = utclocal()
            self.actualizado = self.creado

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'actualizado' with the current datetime"""
        models.storage.new(self)
        models.storage.save()
    
    def registrar(self):
        """registra la instancia en la base de datos. Es otro nombre para el
        método 'save'"""
        self.save()
    
    def update(self, *args, **kwargs):
        """updates the instance based on the keyword passed arguments"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "id" and key != "__class__" and key != "creado" and key != "actualizado":
                    try:
                        setattr(self, key, datetime.strptime(value, ftime))
                    except:
                        setattr(self, key, value)
                else:
                    return -1
        self.actualizado = utclocal()
        models.storage.save()
        return 0


    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "creado" in new_dict:
            new_dict["creado"] = new_dict["creado"].strftime(ftime)
        if "actualizado" in new_dict:
            new_dict["actualizado"] = new_dict["actualizado"].strftime(ftime)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if hasattr(self, "contrasenia"):
            del new_dict["contrasenia"]
        if hasattr(self, "cantidadProductos"):
            new_dict["cantidadProductos"] = json.loads(new_dict["cantidadProductos"])
        if hasattr(self, "fechaEvento"):
            new_dict["fechaEvento"] = new_dict["fechaEvento"].strftime(ftime)
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
