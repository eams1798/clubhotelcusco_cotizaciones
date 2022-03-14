#!/usr/bin/python3
"""Módulo con métodos para convertir un string con el formato: 'arg1=val1 arg2=val2 ...' en un diccionario listo para usar"""


import shlex


def evaluate(value):
    try:
            value = eval(value)
    except:
            value = f'{value}'
    return value


def str_to_dict(args):
    unordered_args = args.split('=')
    dictlist=[]
    for arg in unordered_args:
        if "[" in arg and "]" in arg:
            flag = 0
            string = ""
            for char in arg:
                if char == "[":
                    flag = 1
                if flag == 1:
                    string += char
                if char == "]":
                    flag = 0
                    dictlist.append(string)
                    if char != arg[-1]:
                        dictlist.append(arg.split(' ')[-1])
        elif "{" in arg and "}" in arg:
            flag = 0
            string = ""
            for char in arg:
                if char == "{":
                    flag = 1
                if flag == 1:
                    string += char
                if char == "}":
                    flag = 0
                    dictlist.append(string)
                    if char != arg[-1]:
                        dictlist.append(arg.split(' ')[-1])
        else:
            dictlist.extend(shlex.split(arg))


    keys = dictlist[::2]
    values = dictlist[1::2]

    dictionary = {}
    for idx in range(len(keys)):
        dictionary[keys[idx]] = evaluate(values[idx])
    return dictionary
