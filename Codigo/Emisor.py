import Adafruit_DHT
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
bits=[5,17,18,22,23,24,25,6]
GPIO.setup(bits[0],GPIO.OUT)
GPIO.setup(bits[1],GPIO.OUT)
GPIO.setup(bits[2],GPIO.OUT)
GPIO.setup(bits[3],GPIO.OUT)
GPIO.setup(bits[4],GPIO.OUT)
GPIO.setup(bits[5],GPIO.OUT)
GPIO.setup(bits[6],GPIO.OUT)
GPIO.setup(bits[7],GPIO.OUT)

DHT_Sensor = Adafruit_DHT.DHT11
DHT_Pin = 4

try:
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_Sensor, DHT_Pin)
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
            
            #Conversion del dato de temperatura a numero binario
            temp_int=int(temperature)
            num_bin_inv=''
            while temp_int > 0:
                if temp_int % 2 == 0:
                    temp_int= int(temp_int/2)
                    num_residuo = 1
                    num_bin_inv += '0'
                    
                elif temp_int % 2 ==1:
                    temp_int = int(temp_int/2)
                    num_residuo = 1
                    num_bin_inv += '1'
            temp_bin = num_bin_inv[::-1]
            
            #print(temp_bin)
            
            #Activacion de un led representando al numero binario transformado
            n=len(temp_bin)
            num_bits=(8-n)*'0'+temp_bin
            num_bin_list = list(num_bits)
            m=len(num_bin_list)
            i=0
            for i in range (m-1):
                if num_bin_list[i] == '1':
                    #print ("Es uno")
                    GPIO.output(bits[i], GPIO.HIGH)
                else:
                    #print ("Es cero").
                    GPIO.output(bits[i], GPIO.LOW)
            
            
            
        else:
            print("Falla en la lectura.")
         
        time.sleep(60)
    
except KeyboardInterrupt:
    print("Simulacion interrumpida")
    
finally:
    GPIO.cleanup()
        