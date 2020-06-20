#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Importamos los modulos Requeridos
from pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO
import time
import lcddriver
import datetime
import pymysql

#Definimos la conexion a la base de datos
db = pymysql.connect(
        host="localhost",
        database="biometrico",
        user="administrador",
        password="manex"
)

mysqlcursor = db.cursor()
#Llamamos al lcd
lcd=lcddriver.lcd()

lcdprint=lcd.lcd_display_string

button_1=16 #Definiendo los pines para los botones
button_2=12 #Definiendo los pines para los botones

ledrojo=15 #Definiendo los pines para los leds
ledverde=13 #Definiendo los pines para los leds


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledverde,GPIO.OUT)
GPIO.setup(ledrojo, GPIO.OUT)
GPIO.setup(button_1, GPIO.IN)
GPIO.setup(button_2, GPIO.IN)

GPIO.output(ledrojo,GPIO.LOW)
GPIO.output(ledverde,GPIO.LOW)

lcd.lcd_clear()
GPIO.output(ledverde, GPIO.HIGH)


def menu_bio():
    while True:
        lcdprint('Asistencia ITSG', 1)
        lcdprint(str(datetime.datetime.now()), 2)
        print("""
        1.Registrar
        2.Asistencia
        3.Buscar
        4.Eliminar
        5.Salir
        """)
        op= input("Ingrese:")#GPIO.input(button_1)#True-Presionado  False-Si No Presiona
        while True:
            if op=="1":#True
                GPIO.output(ledverde,GPIO.LOW)
                lcd.lcd_clear()
                register()
                break
            elif op=="2":#True
                GPIO.output(ledverde,GPIO.LOW)
                lcd.lcd_clear()
                delete()
                break
            else:
                print("error")
    

"""registrara los datos de la huella y e informacion adicional
Que sera añadida a la base de datos en la tabla , empleados"""

def register():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if (f.verifyPassword() == False):
            raise ValueError('La Contraseña del sensor de huellas dactilares dada es incorrecta!')
    except Exception as e:
        print('No se puedo inicializar el sensor de huellas dactilares!')
        print('Mensaje de exepcion: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('\tEdu Attendance v1.0')
    print('')
    print('Plantillas utilizada actualmente: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))
    print('')
    
    print("Registrar un Nuevo Usuario")
    new_name = input("Nombre: ")
    result = finger()
    sql = """INSERT INTO empleado ( nombre,id_huella,dato) VALUES ('%s','%s','%s')""" %(new_name,result[0],result[1])
    mysqlcursor.execute(sql)
    db.commit()
    db.rollback()
    print("Completado")
    lcd.lcd_display_string('Completado',1)
    db.close()


"""registrara la asistencia mediante la huella ,
Que sera añadida a la base de datos en la tabla , asistencia"""

def attendance():
    print('\tEdu Attendance v1.0')
    print('')
    lcdprint('Esperando su Huella..',2)
    print("Esperando su Huella...")

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
            ## Wait that finger is read
            prnt = f.readImage()

            if (prnt != False):

                ## Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)

                result = f.searchTemplate()
                positionNumber = f.storeTemplate()
                f.loadTemplate(positionNumber, 0x01)

                positionNumber = result[0]
                mysqlcursor.execute("Select nombre FROM empleado WHERE id_huella = ('%i')" % (positionNumber))
                nombre = mysqlcursor.fetchone()
                sname = nombre[0]
                print("Bienvenido " + sname)

                while True:
                    menuIS()
                    op=input("Ingrese una Opcion")
                    if op=="1":
                        new_status='Ingreso'
                        new_fecha=datetime.datetime.now()
                        sql="""INSERT INTO asistencia(id_empleado,estado,fecha) VALUES 
                        ((SELECT id_empleado FROM empleado WHERE id_bio='%i'),'%s','%s')""" % (positionNumber,new_status,new_fecha)
                        mysqlcursor.execute(sql)
                        db.commit()
                        db.rollback()
                        print("Completado!")
                        db.close()
                        break
                    elif op=="2":
                        new_status='Salida'
                        new_fecha=datetime.datetime.now()
                        sql = """INSERT INTO asistencia(id_docente,estado,fecha) VALUES 
                                                ((SELECT id_docente FROM docente WHERE id_bio='%i'),'%s','%s')""" % (
                        positionNumber, new_status, new_fecha)
                        mysqlcursor.execute(sql)
                        db.commit()
                        db.rollback()
                        print("Completado!")
                        db.close()
                        break
                    else:
                        print("Ingrese una Opcion Correcta")
                    break

                break

        except Exception as e:
            print('No se Encontraron Coincidencias')
            print('Scanea de Nuevo!')

            time.sleep(2)

def search():
    # Search for a finger
    print('\tEdu Attendance v1.0')
    print("")
    print("Esperando su Huella...")
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
            # Wait that finger is read
            prnt = f.readImage()

            if (prnt != False):
                # Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)
                ## Searchs template

                result = f.searchTemplate()

                positionNumber = result[0]

                f.loadTemplate(positionNumber, 0x01)
                mysqlcursor.execute("Select nombre FROM docente WHERE id_bio = ('%i')" % (positionNumber))
                nombre = mysqlcursor.fetchone()
                sname = nombre[0]
                print("Bienvenido " + sname)

                break


        except Exception as e:
            print('No se Encontraron Coincidencias')
            print('Scanea de Nuevo!')

            time.sleep(2)
            
def delete():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('La Contraseña del sensor de huellas dactilares dada es incorrecta!')

    except Exception as e:
        print('No se puedo inicializar el sensor de huellas dactilares!')
        print('Mensaje de exepcion: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('\tEdu Attendance v1.0')
    print('')
    print('Plantillas utilizada actualmente: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))
    print('')
    try:

        if f.clearDatabase()==True:
            print('Plantillas actualmente: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

    except Exception as e:
        print('Operacion fallida')
        print('Mensaje de exepcion: ' + str(e))
        exit(1)
        
def finger():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('La Contraseña del sensor de huellas dactilares dada es incorrecta!')

    except Exception as e:
        print('No se puedo inicializar el sensor de huellas dactilares!')
        print('Mensaje de exepcion: ' + str(e))
        exit(1)

    ## Tries to enroll new finger
    while True:    
        try:
            print('Waiting for finger...')

            ## Wait that finger is read
            while (f.readImage() == False):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)

            ## Checks if finger is already enrolled
            result = f.searchTemplate()
            positionNumber = result[0]
                
            if (positionNumber >= 0):
                print('Template already exists at position #' + str(positionNumber))
                exit(0)

            time.sleep(2)

            print('Waiting for same finger again...')

            ## Wait that finger is read again
            while (f.readImage() == False):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 2
            f.convertImage(0x02)

            ## Compares the charbuffers
            if (f.compareCharacteristics() == 0):
                raise Exception('Fingers do not match')

                print('Fingers do not match',str(positionNumber))
            
            ## Creates a template
            f.createTemplate()

            ## Saves template at new position number

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
            print('Error')
            print('Scanea de Nuevo!')

            time.sleep(2)

if __name__ == '__main__':
    try:
        menu_bio()
    except KeyboardInterrupt:
        pass
