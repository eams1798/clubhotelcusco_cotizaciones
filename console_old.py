#!/usr/bin/python3
"""The HBNB Console"""

import cmd
import sys
import re
import json
from models.engine.db_storage import DBStorage, classes
from models import storage

dictclass = classes


def no_quotes(string):
    """deletes the quotes in a string"""
    if (string[0] == '\"' or string[0] == '\''):
        return string[1:-1]
    else:
        return string


def is_integer(string):
    """checks if a string cotains an integer format"""
    if string[0] == ('-', '+'):
        return string[1:].isdigit()
    else:
        return string.isdigit()


def is_float(string):
    """checks if a string cotains an float format"""
    try:
        float(string)
        return True
    except ValueError:
        return False


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def emptyline(self):
        """Does nothing
        """
        pass

    def do_create(self, line):
        """Creates a new instance of any allowed class
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        else:
            if args[0] in dictclass.keys():

                obj = dictclass[a]()
                obj.save()
                print(obj.id)
            else:
                print("** class doesn't exist **")
                break

    def do_show(self, line):
        """Prints the string representation of an instance of a class
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in dictclass.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all().keys():
            print("** no instance found **")
        else:
            obj = storage.all()[f"{args[0]}.{args[1]}"]
            print(obj)

    def do_all(self, line):
        """Prints all string representation of all instances based or
        not on the class name
        """
        args = line.split()
        listobjs = []
        if len(args) == 0:
            for v in storage.all().values():
                listobjs.append(str(v))
            print(listobjs)
        elif args[0] not in dictclass.keys():
            print("** class doesn't exist **")
        else:
            for k, v in storage.all().items():
                clid = k.split('.')
                if clid[0] == args[0]:
                    listobjs.append(str(v))
            print(listobjs)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in dictclass.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in storage.all().keys():
            print("** no instance found **")
        else:
            obj = storage.all()[f"{args[0]}.{args[1]}"]
            del(obj)
            """deletes the instance"""
            del storage.all()[f"{args[0]}.{args[1]}"]
            """deletes the item in the main dictionary"""
            storage.save()

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding
        or updating attribute

                 args[0] args[1]  args[2]   args[3]   args[4]   ...
        Formato: Objeto  idObjeto atr1=val1 atr2=val2 atr3=val3 ...
        """
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all().keys():
            print("** no instance found **")
        elif len(args) == 2:
            print("** requires at least one attribute name and value **")
        else:
            objU = storage.all()[f"{args[0]}.{args[1]}"]
            atributos = str_to_dict(args[2:])
            if objU.update(**atributos) == -1:
                print("** no se pasaron atributos o uno de los atributos está prohibido de modificarse **")
            print(f"{args[0]}.{args[1]} actualizado correctamente")


    def do_count(self, line):
        """Prints the number of instances of a class, or all instances
        """
        args = line.split()
        listobjs = []
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in dictclass.keys():
            if args[0] == "all":
                n = 0
                for key in storage.all().keys():
                    n = n + 1
                print(str(n))
            else:
                print("** class doesn't exist **")
        else:
            n = 0
            for key in storage.all().keys():
                clid = key.split('.')
                if clid[0] == args[0]:
                    n = n + 1
            print(str(n))

    def default(self, line):
        """Checks a new structure of commands: <class>.<command>(<arguments>)
        """
        m = re.search('[^\(\)\.\s]+\.[^\(\)\.\s]+\([^\(\)]*\)', line)
        if m is not None:
            found = re.findall('[^\(\)]*', line)
            clcmd = found[0].split('.')
            argcmd = clcmd[1]
            if hasattr(self, 'do_' + argcmd):
                argclass = clcmd[0]
                linearg = found[2]
                rep = linearg.replace("'", "\"")
                id_dict = re.findall('[^\{\}]*', rep)
                try:
                    dictarg = "{" + id_dict[2] + "}"
                    dictarg = json.loads(dictarg)
                    classid = id_dict[0].replace("\"", "").replace(",", "")
                    argclass += " {}".format(classid)
                    if argcmd == "update":
                        self.dict_update(argclass, **dictarg)
                    else:
                        self.stdout.write('*** Unknown syntax: %s\n'%line)
                except IndexError:
                    itemstr = linearg.split(", ")
                    args = ""
                    for i in range(len(itemstr)):
                        if i != 2:
                            args += itemstr[i].replace("\"", "") + " "
                        else:
                            args += itemstr[i] + " "
                    newl = "{} {} {}".format(argcmd, argclass, args)
                    self.onecmd(newl)
                except json.decoder.JSONDecodeError:
                    print("** Invalid format **")
            else:
                self.stdout.write('*** Unknown syntax: %s\n'%line)
        else:
            self.stdout.write('*** Unknown syntax: %s\n'%line)

    def do_EOF(self, line):
        """EOF command to exit the program
        """
        sys.exit(0)

    def do_quit(self, line):
        """Quit command to exit the program
        """
        sys.exit(0)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
