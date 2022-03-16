#!/usr/bin/python3
"""The HBNB Console"""

import cmd
import sys
import re
import json
import shlex
from strdict import str_to_dict
from models.engine.db_storage import DBStorage, classes
from models import storage
import pdb

dictclass = classes


class CMDClubHotelCusco(cmd.Cmd):
    prompt = 'HotelCusco >> '

    def emptyline(self):
        """Si no se pasa ningun comando en el shell, no hace nada
        """
        pass
    
    def do_productos(self, line):
        """metodo de prueba para las cotizaciones"""
        arguments = line.split()
        obj = storage.all()[f"{arguments[0]}.{arguments[1]}"]
        print(obj.productos)
    
    
    def do_cotizaciones(self, line):
        """metodo de prueba para los productos y clientes"""
        arguments = line.split()
        obj = storage.all()[f"{arguments[0]}.{arguments[1]}"]
        print(obj.cotizaciones)


    def do_crear(self, line):
        """Crea una nueva instancia de cualquier clase permitida

                 arguments[0] arguments[1]   arguments[2]   arguments[3]
        Formato: Clase   atr1=val1 atr2=val2 atr3=val3 ...
        """
        arguments = shlex.split(line)
        if len(arguments) == 0:
            print("** falta el nombre de la clase **")
        else:
            nombreClase = arguments[0]
            flag = 0
            line = line[len(arguments[0]) + 1:]
            for arg in arguments[1:]:
                if "=" not in arg and "," not in arg and ":" not in arg and "{" not in arg and "}" not in arg:
                    print("** argumento incorrecto **")
                    flag = -1
                    break
            if flag == 0:
                # pdb.set_trace()
                atributos = str_to_dict(line)
                if arguments[0] in dictclass.keys():
                    obj = dictclass[nombreClase](**atributos)
                    obj.save()
                    print(obj.id)
                else:
                    print("** la clase no existe **")

    def do_mostrar(self, line):
        """Imprime una instancia de clase

                 arguments[0] arguments[1]
        Formato: Clase   idInstancia
        """
        arguments = line.split()
        if len(arguments) == 0:
            print("** falta el nombre de la clase **")
        elif arguments[0] not in dictclass.keys():
            print("** la clase no existe **")
        elif len(arguments) == 1:
            print("** falta la id de la instancia **")
        # pdb.set_trace()
        # print(f"{arguments[0]}.{arguments[1]}")
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print("** no instance found **")
        else:
            obj = storage.all()[f"{arguments[0]}.{arguments[1]}"]
            print(obj)

    def do_mostrarTodo(self, line):
        """Imprime todos los objetos de una clase o todos los objetos

                 arguments[0]
        Formato: Clase(opcional)
        """
        arguments = line.split()
        listobjs = []
        if len(arguments) == 0:
            for v in storage.all().values():
                listobjs.append(str(v))
            print(listobjs)
        elif arguments[0] not in classes.keys():
            print("** la clase no existe **")
        else:
            for k, v in storage.all().items():
                clid = k.split('.')
                if clid[0] == arguments[0]:
                    listobjs.append(str(v))
            print(listobjs)

    def do_borrar(self, line):
        """Borra una instancia de clase basada en su id

                 arguments[0] arguments[1]
        Formato: Clase   idInstancia
        """
        arguments = line.split()
        if len(arguments) == 0:
            print("** falta el nombre de la clase **")
        elif arguments[0] not in dictclass.keys():
            print("** la clase no existe **")
        elif len(arguments) == 1:
            print("** falta la id de la instancia **")
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print("** id incorrecto: no se encontró la instancia **")
        else:
            # pdb.set_trace()
            storage.delete(storage.all()[f"{arguments[0]}.{arguments[1]}"])
            """Borra el objeto en su diccionario de clases principales"""
            storage.save()

    def do_actualizar(self, line):
        """Actualiza una instancia de clase basada en los atributos pasados

                 arguments[0] arguments[1]    arguments[2]   arguments[3]   arguments[4]   ...
        Formato: Clase  idInstancia atr1=val1 atr2=val2 atr3={key1: val2} ...
        """
        arguments = shlex.split(line)
        if len(arguments) == 0:
            print("** falta el nombre de la clase **")
        elif arguments[0] not in classes.keys():
            print("** la clase no existe **")
        elif len(arguments) == 1:
            print("** falta la id de la instancia **")
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print("** id incorrecto: no se encontró la instancia **")
        elif len(arguments) == 2:
            print("** requiere al menos un nombre de atributo y un valor **")
        else:
            objU = storage.all()[f"{arguments[0]}.{arguments[1]}"]
            flag = 0
            line = line[len(arguments[0]) + len(arguments[1]) + 2:]
            for arg in arguments[2:]:
                if "=" not in arg and "," not in arg and ":" not in arg and "{" not in arg and "}" not in arg:
                    print("** argumento incorrecto **")
                    flag = -1
                    break
            if flag == 0:
                atributos = str_to_dict(line)
                # pdb.set_trace()
                updatestat = objU.update(**atributos)
                if updatestat == -1:
                    print("** no se pasaron atributos o uno de los atributos está prohibido de modificarse **")
                else:
                    print(f"{arguments[0]}.{arguments[1]} actualizado correctamente")


    def do_contar(self, line):
        """Imprime la cantidad de instancias de una clase, o de todas las clases

                 arguments[0]
        Formato: Clase
        """
        arguments = line.split()
        listobjs = []
        if len(arguments) == 0:
            print("** falta el nombre de la clase **")
        elif arguments[0] not in dictclass.keys():
            if arguments[0] == "todo":
                n = 0
                for key in storage.all().keys():
                    n = n + 1
                print(str(n))
            else:
                print("** la clase no existe **")
        else:
            n = 0
            for key in storage.all().keys():
                cls_id = key.split('.')
                if cls_id[0] == arguments[0]:
                    n = n + 1
            print(str(n))

    def do_EOF(self, line):
        """Sale del programa
        """
        sys.exit(0)

    def do_quit(self, line):
        """Sale del programa
        """
        sys.exit(0)


if __name__ == '__main__':
    CMDClubHotelCusco().cmdloop()
