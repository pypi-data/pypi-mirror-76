# conding:utf-8

import os
import re
import time
import serial

import numpy as np

def ScannerCode(ser1, ser2):
    try:
        
        if ser1 and ser1.isOpen == False:       
            #print('ser1 open')     
            ser1.open()  
            
        if ser2 and ser2.isOpen == False:            
            ser2.open()  

        if ser1:
            #print('ser1 scan') 
            #ser1.write("^_^MDTDTO10. \n".encode("utf-8"))
            ser1.write("^_^SCAN. \n".encode("utf-8"))  # 位置3

        if ser2:
            #ser2.write("^_^MDTDTO10. \n".encode("utf-8"))
            ser2.write("^_^SCAN. \n".encode("utf-8"))  # 位置3

        code = ''

        while True:
            
            

            if ser1:
                count = ser1.inWaiting()  # 位置4
                #print(count)
                if count>10:
                    recv = ser1.read(count)  # 位置5
                    print("Recv some data is : ",recv)
                    recv = str(recv,'utf-8')

                    arr = recv.split('/')
                    index = len(arr)-1
                   
                    #print("rqcode data is: ",arr[index])
                    code = arr[index]
                    ser1.flushInput()
                    break
              
                ser1.flushInput()
                

            if ser2:
                count2 = ser2.inWaiting()  # 位置4
                
                if count2>10:
                    recv2 = ser2.read(count)  # 位置5
                    print("Recv some data is : ",recv2)
                    recv2 = str(recv2,'utf-8')

                    arr = recv2.split('/')
                    index = len(arr)-1
                   
                    #print("rqcode data is: ",arr[index])
                    ser2.flushInput()
                    code = arr[index]
                    break
              
                ser2.flushInput()
                
            
            time.sleep(0.1)
        

        return code

    except Exception as e:
        print(e)
        return "error"

def FengMing(ser1,ser2):
    try:
        
        if ser1 and ser1.isOpen == False:       
            #print('ser1 open')     
            ser1.open()  
            
        if ser2 and ser2.isOpen == False:            
            ser2.open()  

        if ser1:
            #print('ser1 scan') 
            #ser1.write("^_^MDTDTO10. \n".encode("utf-8"))
            ser1.write("^_^BEPP9. \n".encode("utf-8"))  # 位置3
            time.sleep(1)
            #ser1.write("^_^BEPPWR0. \n".encode("utf-8"))  # 位置3

        if ser2:
            #ser2.write("^_^MDTDTO10. \n".encode("utf-8"))
            ser1.write("^_^BEPP9. \n".encode("utf-8"))  # 位置3
            time.sleep(1)
            #ser1.write("^_^BEPPWR0. \n".encode("utf-8"))  # 位置3

        print('ok')
        

    except Exception as e:
        print(e)

def getDevNames():
    
    devs = []

    dirs= os.listdir("/dev")

    for name in dirs :
        #print(a)
        
        matchObj = re.match( r'ttyACM\d', name)
        if matchObj:
            #print(name) #当前路径下所有非目录文件
            devs.append(name)

    return devs
    

if __name__ == "__main__":
    names = getDevNames()

    ser1 = None
    ser2 = None

    #print(names,names[0])
    print("/dev/{0}".format(names[0]))

    if len(names) == 1:
        ser1 = serial.Serial("/dev/{0}".format(names[0]), 9600)  # 位置1
    elif len(names) == 2:
        ser1 = serial.Serial("/dev/{0}".format(names[0]), 9600)  # 位置1
        ser2 = serial.Serial("/dev/{0}".format(names[1]), 9600)  # 位置1

    # FengMing(ser1,ser2)
    
    code = ScannerCode(ser1, ser2)
    print(code)
    

