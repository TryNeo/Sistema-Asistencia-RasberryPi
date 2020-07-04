import RPi.GPIO as GPIO

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

