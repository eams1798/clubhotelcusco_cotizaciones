#!/usr/bin/python3
"""Establece variables de entorno para acceder a la base de datos.
El modo de desarrollo estará activado por defecto
Para cambiar al modo de prueba, escriba en la línea de comandos 'mode=test'
sin las comillas, antes de ejecutar este módulo o importarlo a otro
"""

from os import environ, getenv

environ['HC_MYSQL_HOST'] = 'localhost'

if getenv('mode') == 'test':
    environ['HC_MYSQL_USER'] = 'clubhotelcuscot'
    environ['HC_MYSQL_PWD'] = '951chctpwd753'
    environ['HC_ENV'] = 'test'
    environ['HC_MYSQL_DB'] = 'clubhotelcusco_test_db'
else:
    environ['HC_MYSQL_USER'] = 'clubhotelcusco'
    environ['HC_MYSQL_PWD'] = '951chcpwd753'
    environ['HC_ENV'] = 'dev'
    environ['HC_MYSQL_DB'] = 'clubhotelcusco_db'

if __name__ == '__main__':
    print(f'user: {getenv("HC_MYSQL_USER")}\
            \npassword: {getenv("HC_MYSQL_PWD")}\
            \nhost: {getenv("HC_MYSQL_HOST")}\
            \nenvirnonment: {getenv("HC_ENV")}\
            \ndatabase: {getenv("HC_MYSQL_DB")}')
