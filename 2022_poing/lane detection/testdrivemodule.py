import motors as mot
import keyboardmodule as km
import serial
import time
var = 0
ser = serial.Serial(port = "/dev/ttyACM0",baudrate = 9600,)
time.sleep(1)
km.init()

while True:
    val = '9'
    if km.getKey('w'):
        print('forward')
        val = '2' 
        
    
    elif km.getKey('s'):
        print('backward')
        val = '5' 
        
   
    elif km.getKey('q'):
        print('fleft')
        val = '1' 
        
      
    elif km.getKey('e'):
        print('fright')
        val = '3' 
        
    
    elif km.getKey('a'):
        print('bleft')
        val = '2' 
       
       
    elif km.getKey('d'):
        print('bright')
        val = '6' 
    
    elif km.getKey('f'):
        print('stop')
        val = '0'  

    ser.write(val.encode())
