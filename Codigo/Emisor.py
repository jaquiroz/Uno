import Adafruit_DHT
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.output(5,GPIO.LOW)
GPIO.output(6,GPIO.LOW)
DHT_Sensor = Adafruit_DHT.DHT11
DHT_Pin = 4

try:
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_Sensor, DHT_Pin)
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
            #print(humidity)
            GPIO.output(6,GPIO.HIGH)
            GPIO.output(5,GPIO.LOW)
        else:
            print("Falla en la lectura.")
            GPIO.output(5,GPIO.HIGH)
            GPIO.output(6,GPIO.LOW)
        
        time.sleep(5)
    
except KeyboardInterrupt:
    print("Simulacion interrumpida")
    
finally:
    GPIO.cleanup()
        