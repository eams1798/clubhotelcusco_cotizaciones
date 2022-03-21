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
from cstr import cstr
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
        if len(arguments) == 0:
            print(cstr("** falta el nombre de la clase **").color('red'))
        elif arguments[0] != "Cotizacion":
            print(cstr("** clase no permitida para este comando **").color('red'))
        elif len(arguments) == 1:
            print(cstr("** falta la id de la instancia **").color('red'))
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print(cstr("** id incorrecto: no se encontró la instancia **").color('red'))
        else:
            obj = storage.all()[f"{arguments[0]}.{arguments[1]}"]
            idObj = [prod.id for prod in obj.productos]
            printed = cstr(idObj).color('green')
            print(printed)
    
    
    def do_cotizaciones(self, line):
        """metodo de prueba para los productos y clientes"""
        arguments = line.split()
        if len(arguments) == 0:
            print(cstr("** falta el nombre de la clase **").color('red'))
        elif arguments[0] != "Producto" and arguments[0] != "Cliente":
            print(cstr("** clase no permitida para este comando **").color('red'))
        elif len(arguments) == 1:
            print(cstr("** falta la id de la instancia **").color('red'))
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print(cstr("** id incorrecto: no se encontró la instancia **").color('red'))
        else:
            obj = storage.all()[f"{arguments[0]}.{arguments[1]}"]
            idObj = [prod.id for prod in obj.cotizaciones]
            printed = cstr(idObj).color('green')
            print(printed)


    def do_crear(self, line):
        """Crea una nueva instancia de cualquier clase permitida

                 arguments[0] arguments[1]   arguments[2]   arguments[3]
        Formato: Clase   atr1=val1 atr2=val2 atr3=val3 ...
        """
        arguments = shlex.split(line)
        if len(arguments) == 0:
            print(cstr("** falta el nombre de la clase **").color('red'))
        else:
            nombreClase = arguments[0]
            flag = 0
            line = line[len(arguments[0]) + 1:]
            for arg in arguments[1:]:
                if "=" not in arg and "," not in arg and ":" not in arg and "{" not in arg and "}" not in arg:
                    print(cstr("** argumento incorrecto **").color('red'))
                    flag = -1
                    break
            if flag == 0:
                # pdb.set_trace()
                atributos = str_to_dict(line)
                if arguments[0] in dictclass.keys():
                    obj = dictclass[nombreClase](**atributos)
                    obj.save()
                    printed = cstr(obj.id).color('green')
                    print(printed)
                else:
                    print(cstr("** la clase no existe **").color('red'))

    def do_mostrar(self, line):
        """Imprime una instancia de clase

                 arguments[0] arguments[1]
        Formato: Clase   idInstancia
        """
        arguments = line.split()
        if len(arguments) == 0:
            print(cstr("** falta el nombre de la clase **").color('red'))
        elif arguments[0] not in dictclass.keys():
            print(cstr("** la clase no existe **").color('red'))
        elif len(arguments) == 1:
            print(cstr("** falta la id de la instancia **").color('red'))
        # pdb.set_trace()
        # print(f"{arguments[0]}.{arguments[1]}")
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print(cstr("** id incorrecto: no se encontró la instancia **").color('red'))
        else:
            obj = storage.all()[f"{arguments[0]}.{arguments[1]}"]
            printed = cstr(obj).color('green')
            print(printed)

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
            print(cstr(listobjs).color('green'))
        elif arguments[0] not in classes.keys():
            print(cstr("** la clase no existe **").color('red'))
        else:
            for k, v in storage.all().items():
                clid = k.split('.')
                if clid[0] == arguments[0]:
                    listobjs.append(str(v))
            printed = cstr(listobjs).color('green')
            print(printed)

    def do_borrar(self, line):
        """Borra una instancia de clase basada en su id

                 arguments[0] arguments[1]
        Formato: Clase   idInstancia
        """
        arguments = line.split()
        if len(arguments) == 0:
            print(cstr("** falta el nombre de la clase **").color('red'))
        elif arguments[0] not in dictclass.keys():
            print(cstr("** la clase no existe **").color('red'))
        elif len(arguments) == 1:
            print(cstr("** falta la id de la instancia **").color('red'))
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print(cstr("** id incorrecto: no se encontró la instancia **").color('red'))
        else:
            # pdb.set_trace()
            if arguments[0] == "Producto":
                obj = storage.all()[f"{arguments[0]}.{arguments[1]}"]
                for cotizacion in obj.cotizaciones:
                    cantProductos = cotizacion.getCantidadProductos()
                    del cantProductos[obj.id]
                    cotizacion.actualizarProductos(**cantProductos)
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
            print(cstr("** falta el nombre de la clase **").color('red'))
        elif arguments[0] not in classes.keys():
            print(cstr("** la clase no existe **").color('red'))
        elif len(arguments) == 1:
            print(cstr("** falta la id de la instancia **").color('red'))
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all().keys():
            print(cstr("** id incorrecto: no se encontró la instancia **").color('red'))
        elif len(arguments) == 2:
            print(cstr("** requiere al menos un nombre de atributo y un valor **").color('red'))
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
                    print(cstr("** no se pasaron atributos o uno de los atributos está prohibido de modificarse **").color('red'))
                else:
                    print(cstr(f"{arguments[0]}.{arguments[1]} actualizado correctamente").color('green'))


    def do_contar(self, line):
        """Imprime la cantidad de instancias de una clase, o de todas las clases

                 arguments[0]
        Formato: Clase
        """
        arguments = line.split()
        listobjs = []
        if len(arguments) == 0:
            print(cstr("** falta el nombre de la clase **").color('red'))
        elif arguments[0] not in dictclass.keys():
            if arguments[0] == "todo":
                n = 0
                for key in storage.all().keys():
                    n = n + 1
                print(cstr(n).color('green'))
            else:
                print(cstr("** la clase no existe **").color('red'))
        else:
            n = 0
            for key in storage.all().keys():
                cls_id = key.split('.')
                if cls_id[0] == arguments[0]:
                    n = n + 1
            print(cstr(n).color('green'))

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
