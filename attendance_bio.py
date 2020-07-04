#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Importamos los modulos Requeridos
import RPi.GPIO as GPIO
import time
import datetime

#modulos externos
from lib.lcddriver import *
from conexiones.connect_mariadb import *
from lib.pyfingerprint import PyFingerprint

#defiendo el curspr para el bd
mysqlcursor = mydb.cursor()


#Llamamos al lcd
lcd = lcd.lcd()
lcdprint = lcd.lcd_display_string

BUTTON_1 = 16 #Definiendo los pines para los botones
BUTTON_2 = 12 #Definimos los pines para los botones

LED_VERDE = 13  #Definiendo los pines para los leds
LED_ROJO = 15 #Definiendo los pines para los leds

GPIO.setwarnings(False) #poniendo en off el debug
GPIO.setmode(GPIO.BOARD) #colocamos el modo BOARD
GPIO.setup(LED_VERDE,GPIO.OUT) #asignamos los pines - color verde
GPIO.setup(LED_ROJO,GPIO.OUT) #asignamos los pines -- color rojo
GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #asignamos el button 1
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #asignamos el button 2

GPIO.output(LED_VERDE,GPIO.LOW)
GPIO.output(LED_ROJO,GPIO.LOW)

#limpiando pantalla LCD
lcd.lcd_clear()
GPIO.output(LED_VERDE,GPIO.HIGH)


#Definiendo la conexion con el biometrico
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if (f.verifyPassword() == False):
        raise ValueError('La Contraseña del sensor de huellas dactilares dada es incorrecta!')
except Exception as e:
    print('No se puedo inicializar el sensor de huellas dactilares!')
    print('Mensaje de exepcion: ' + str(e))
    exit(1)



"""
Defiendo la funcion menu_bio para presentarse en LCD
"""
def menu_bio():
    def read(estado):
        try:
            prnt = f.readImage()
            if (prnt != False):
                f.convertImage(0x01)
                
                result = f.searchTemplate()
                #positionNumber = f.storeTemplate()
                #f.loadTemplate(positionNumber, 0x01)
                #positionNumber = result[0]
                
                print(result[0])
                
                mysqlcursor.execute("Select nombre FROM empleado WHERE id_huella = ('%i')" % (result[0]))
                nombre = mysqlcursor.fetchone()
                sname = nombre[0]
                print(sname)
                
                status= estado
                date = datetime.datetime.now()
                sql = """INSERT INTO asistencia(id_empleado,id_estado,fecha) VALUES 
                ((SELECT id_empleado FROM empleado WHERE id_huella='%i'),'%s','%s')""" % (result[0],status,date)
                mysqlcursor.execute(sql)
                mydb.commit()
                mydb.rollback()
                lcd.lcd_clear()
                lcdprint(sname,1)
                lcdprint("Success!",2)
                time.sleep(1)
                
        except Exception as e:
            lcdprint('No Hay Coincidencias',1)
            lcdprint('Scanea de Nuevo!',2)
            time.sleep(1)
            lcd.lcd_clear()

            
    estatus=1
    #Declarando un ciclo infinito            
    while True:
        lcdprint('Asistencia ITSG', 1)
        lcdprint(str(datetime.datetime.now()), 2)
        
        inputValue = GPIO.input(BUTTON_1)
        inputValue2= GPIO.input(BUTTON_2)
        
        read(estatus)
    
        if inputValue == GPIO.HIGH:
            GPIO.output(LED_ROJO,GPIO.LOW)
            GPIO.output(LED_VERDE,GPIO.HIGH)
            print("ingreso")
            time.sleep(1)
            estatus=1
            
        if inputValue2 == GPIO.HIGH:
            GPIO.output(LED_VERDE,GPIO.LOW)
            GPIO.output(LED_ROJO,GPIO.HIGH)
            print("salida")
            estatus=2
            time.sleep(1)


if __name__ == '__main__':
    try:
        menu_bio()
    except KeyboardInterrupt:
        pass

