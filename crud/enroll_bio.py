#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.pyfingerprint import PyFingerprint
from conexiones.connect_odoo import *
import xmlrpc.client
import pyfiglet
import time


uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def main():
    ascii_banner = pyfiglet.figlet_format("Edu_Attendance")
    print(ascii_banner)
    menu = 0
    menu_str = """
    1. Ingresar Huella
    2. Salir
    """
    while menu != '2':
        print(menu_str)
        menu = input("Seleccione una opción del menu: ")
        if menu == '1':
            register()
        elif menu=='2':
            print("Good bye!!! See you later.")
            break
        else:
            print("opcion incorrecta - Intente de Nuevo")


def register():
    cedula = input("Ingrese cédula del docente: ")
    faculty_id = models.execute_kw(db, uid, password,
                                   'edu.faculty', 'search',
                                   [[['ced_ruc', '=', cedula]]],
                                   {'limit': 1})
    if faculty_id:
        nombre = models.execute_kw(db, uid, password,
                                   'edu.faculty', 'read',
                                   [faculty_id], {'fields': ['name']})
        print("\nDocente encontrado")
        print(nombre[0]['name'])
        print("\nIngrese su huella dactilar")
        result = finger()
        models.execute_kw(db, uid, password,
                          'edu.faculty', 'write',
                          [[faculty_id[0]], {'finger_print': result[1]}])
                          # [[faculty_id[0]], {'finger_print_id':result[0],'finger_print': result[1]}])
    else:
        print("Docente no encontrado")

def finger():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('La Contraseña del sensor de huellas dactilares dada es incorrecta!')

    except Exception as e:
        print('No se puedo inicializar el sensor de huellas dactilares!')
        print('Mensaje de exepcion: ' + str(e))
        exit(1)

    while True:
        try:
            print('Esperando Huella...')
            while (f.readImage() == False):
                pass
            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]
            if (positionNumber >= 0):
                print('El ID' + str(positionNumber)+'Ya Existe Intente de Nuevo')
            time.sleep(2)

            print('Esperando La misma Huella Otra vez...')

            while (f.readImage() == False):
                pass
            f.convertImage(0x02)

            if (f.compareCharacteristics() == 0):
                raise Exception('La Huella No Coinciden')
                print('La Huella No Coinciden',str(positionNumber))


            f.createTemplate()
            positionNumber = f.storeTemplate()
            f.loadTemplate(positionNumber, 0x01)
            char_store = str(f.downloadCharacteristics(0x01))
            char_store1 = char_store.translate("")
            var = ''
            for x in char_store1:
                var += x
            return positionNumber,var
            break
        
        except Exception as e:
            print("Error de  Huella")
            print('Scanea de Nuevo')
            time.sleep(2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

