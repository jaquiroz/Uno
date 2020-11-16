import Adafruit_DHT
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
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
            
            #Codificacion Manchester Diferencial
            
            n=len(temp_bin)
            temp_bin=(10-n)*'0'+temp_bin
            temp_bin_inv= temp_bin[::-1]
            temp_bin_inv_list = list(temp_bin_inv)
            n_temp_bin_inv_list =len(temp_bin_inv_list)
            man_diff=n_temp_bin_inv_list*['']
            dat='01'

            if temp_bin_inv_list[1] == '0': #Primera condicion de Manchester Diferencial
                man_diff[0]=dat[::-1]
            elif temp_bin_inv_list[1] == '1':
                man_diff[0]=dat

            i=1

            while i<= n_temp_bin_inv_list - 1: #Sigue la regla de Manchester Diferencial para los siguientes terminos
                if temp_bin_inv_list[i] =='0':
                    man_diff[i]=man_diff[i-1]
    
                elif temp_bin_inv_list[i] == '1':
                    aux=man_diff[i-1]
                    man_diff[i]=aux[::-1]
        
                i+=1

            man_diff_str=''

            for i in range(n_temp_bin_inv_list):
                man_diff_str+=str(man_diff[i])
    
            man_diff_str='0'+man_diff_str+'1'
            man_diff_list=list(man_diff_str)
    
            print(temp_bin)
            print(man_diff_list)
            
            for i in man_diff_list:
                if i == '1':
                    #print ("Es uno")
                    GPIO.output(5, GPIO.HIGH)
                    time.sleep(1)
                else:
                    #print ("Es cero").
                    GPIO.output(5, GPIO.LOW)
                    time.sleep(1)
            
        else:
            print("Falla en la lectura.")
         
        time.sleep(60)
    
except KeyboardInterrupt:
    print("Simulacion interrumpida")
    
finally:
    GPIO.cleanup()
        