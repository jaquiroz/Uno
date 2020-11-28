import serial
import time

serialArduino = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=3.0)
time.sleep(1)

while True:
    cad = serialArduino.readline().decode('ascii')
    
    #cad = serialArduino.readline().decode('utf-8')
    cad1=int(cad)
    mensaje=[]
    mensaje_aux=[]
    if cad1<=80:
        print("Lectura")
        for i in range(21):
            aux_string = serialArduino.readline().decode('ascii')
            aux_int=int(aux_string)
            mensaje_aux.append(aux_int)

        for j in mensaje_aux:
            if j<=80:
                mensaje.append(0)
            else:
                mensaje.append(1)
        #mensaje.append(1)#Inclusion de bit de parada   
        #Eliminamos los bits de inicio y parada
        mens_ip=mensaje[0:20]
        temp=[]
        #Conversion de Machester Diferencial a Binario
        copia=mens_ip[::-1]#Creamos una copia del mensaje sin bits de inicio y parada
        i=0
        for i in range(9):
            aux1=copia[2*i:2+2*i]
            aux2=copia[2+2*i:4+2*i]
    
            if aux1==aux2:
                temp.append(0)
            else:
                temp.append(1)
                    
        #Inclusion del primer bit del mensaje segun la conveniencia de Manchester Diferencial                
        dat=[0,1]
        aux=mens_ip[0:2]
        if aux==dat:
            temp.append(1)
        else:
            temp.append(0)
                
        #Conversion de Binario a Decimal
        i=0
        j=9
        decimal=0
        for i in range(10):
            decimal+=temp[i]*pow(2,j)
            j-=1

        print(mens_ip)
        print(temp)
        print("El numero decimal es:")
        print(decimal)
        print("******************************************'")
        

