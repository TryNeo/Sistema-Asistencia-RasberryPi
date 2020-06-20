from lib.pyfingerprint import PyFingerprint
from conexiones.connect_mysql import *
mysqlcursor = mydb.cursor()

def sync_fingerprint():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('La Contraseña del sensor de huellas dactilares dada es incorrecta!')

    except Exception as e:
        print('No se puedo inicializar el sensor de huellas dactilares!')
        print('Mensaje de exepcion: ' + str(e))
        exit(1)

    mysqlcursor.execute("Select id_huella,dato from empleado")

    for empleado in mysqlcursor:
        datos = empleado[1].replace("[","").replace("]","").split(",")
        huella = []
        for dato in datos:
            huella.append(int(dato))
        f.uploadCharacteristics(0x01 ,huella)
        f.storeTemplate(int(empleado[0]))
        print(empleado)