import serial
import time

serialArduino = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=3.0)
time.sleep(1)

while True:
    cad = serialArduino.readline().decode('utf-8')
    print(cad)
    print(type(cad))
    print("****************************")
