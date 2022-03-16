#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models.engine.environ_variables
import models
from models.base_model import BaseModel, Base
from models.cliente import Cliente
from models.cotizacion import Cotizacion
from models.persona import Persona
from models.plantilla import Plantilla
from models.producto import Producto
from models.proveedor import Proveedor
from models.usuario import Usuario
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pdb

classes = {"Cliente": Cliente, "Cotizacion": Cotizacion,
           "Plantilla": Plantilla, "Producto": Producto,
           "Proveedor": Proveedor, "Usuario": Usuario}

class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = getenv('HC_MYSQL_USER')
        password = getenv('HC_MYSQL_PWD')
        host = getenv('HC_MYSQL_HOST')
        db = getenv('HC_MYSQL_DB')
        env = getenv('HC_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, db))
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary from a database query"""
        # pdb.set_trace()
        clsDict = {}
        if cls:
            if cls in classes.keys() or cls in classes.values():
                lstobj = self.__session.query(eval(cls)).all()
                for obj in lstobj:
                    clsname = type(obj).__name__
                    clsstr = "{}.{}".format(clsname, obj.id)
                    clsDict[clsstr] = obj
            else:
                return None
        else:
            for sub_c in classes.keys() or sub_c in classes.values():
                table = self.__session.query(eval(sub_c)).all()
                for obj in table:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    clsDict[key] = obj
        return clsDict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """A method to retrieve one object"""
        if cls in classes.values() and id and type(id) == str:
            objects = self.all(cls)
            for key, value in objects.items():
                if key.split(".")[1] == id:
                    return value
        return None

    def count(self, cls=None):
        """Count objects"""
        if cls in classes.keys() or cls in classes.values():
            objects = self.all(cls)
        else:
            objects = self.all()
        return len(objects)
