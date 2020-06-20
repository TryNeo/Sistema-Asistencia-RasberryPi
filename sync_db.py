#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crud.upload_bio import *
from conexiones.connect_mysql import *
from conexiones.connect_odoo import *
import pyfiglet
import xmlrpc.client

mysqlcursor = mydb.cursor()


def menu_sync():
    ascii_banner = pyfiglet.figlet_format("Sync_db")
    print(ascii_banner)
    menu = 0
    menu_str = """
    1.Dowload Data
    2.Sync FingerPrint
    3.Salir
    """
    while menu != '3':
        print(menu_str)
        menu = input("Seleccione una opción del menu : ")
        if menu == '1':
            # descargar la data de la bd de itsgg y lo ingresa en la bd biometrico
            download_data()
        elif menu=='2':
            # sincronizar base de datos con hardware fingerprint
            sync_fingerprint()
        elif menu=='3':
            print("Good Bye!")
            break
        else:
            print("opcion incorrecta - Intente de Nuevo")


def download_data():
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    faculty_ids = models.execute_kw(db, uid, password,
                                    'edu.faculty', 'search',
                                    [[]])

    faculties = models.execute_kw(db, uid, password,
                                  'edu.faculty', 'read',
                                  [faculty_ids], {'fields': ['id', 'finger_print', 'name', 'finger_print_id']})

    # guardar en base de datos
    for faculty in faculties:
        id_huella =faculty['finger_print_id']
        if(faculty['finger_print_id']!= -1):
            sql = """INSERT INTO empleado( id_empleado,nombre,id_huella,dato)
            VALUES (%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE dato = %s,id_huella = %s
            """


            val = (faculty['id'], faculty['name'], id_huella,
                   faculty['finger_print'], faculty['finger_print'],id_huella)


            mysqlcursor.execute(sql, val)
            mydb.commit()
            print(faculty['name'], faculty['id'], faculty['finger_print'], faculty['finger_print_id'])



if __name__ == '__main__':
    try:
        menu_sync()
    except KeyboardInterrupt:
        pass
