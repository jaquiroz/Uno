from tkinter import Frame,Label,Button,Checkbutton,Scale,StringVar,IntVar
import serial
import time
import threading


class MainFrame(Frame):

    def __init__(self, master=None):
        super().__init__(master, width=480, height=320)                
        self.master = master    
        self.master.protocol('WM_DELETE_WINDOW',self.askQuit)
        self.pack()
        self.hilo1 = threading.Thread(target=self.getSensorValues,daemon=True)
        self.arduino = serial.Serial("/dev/ttyACM0", baudrate=9600,timeout=1.0)
        time.sleep(1)
        self.value_mens_ip = StringVar()
        self.value_temp = StringVar()
        self.value_decimal= IntVar()
        self.value_led = IntVar()
        self.create_widgets()
        self.isRun=True
        self.hilo1.start()

    def askQuit(self):
        self.isRun=False
        self.arduino.write('led:0'.encode('ascii'))
        self.arduino.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print("*** finalizando...")

    def getSensorValues(self):
        while self.isRun:
            cad = self.arduino.readline().decode('ascii')
            #cad = serialArduino.readline().decode('utf-8')
            cad1=int(cad)
            mensaje=[]
            mensaje_aux=[]
            if cad1<=80:
                #print("Lectura")
                for i in range(21):
                    aux_string = self.arduino.readline().decode('ascii')
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
                mens_aux=mensaje
                mens_aux=mens_aux[::-1]
                mens_aux.append(0)
                mens_aux=mens_aux[::-1]
                str_mens_aux="".join(map(str, mens_aux))
                str_temp="".join(map(str, temp))
                self.value_mens_ip.set(str_mens_aux)
                self.value_temp.set(str_temp)
                self.value_decimal.set(decimal)
                

            
        

        
    def fEnviaLed(self):
        cad='led:' + str(self.value_led.get())
        self.arduino.write(cad.encode('ascii'))
        print(cad)


        
    def create_widgets(self):
        Label(self,text="Manchester: ").place(x=30,y=20)
        Label(self,width=22,textvariable=self.value_mens_ip).place(x=30,y=40)
        Label(self,text="Binario: ").place(x=30,y=60)
        Label(self,width=10,textvariable=self.value_temp).place(x=30,y=80)
        Label(self,text="Temperatura: ").place(x=30,y=100)
        Label(self,width=6,textvariable=self.value_decimal).place(x=30,y=120)
        Checkbutton(self, text="Encender/Apagar Ventilador", variable=self.value_led,
        onvalue=1, offvalue=0,command=self.fEnviaLed).place(x=30, y=140)                 
        
        
        

      

        
