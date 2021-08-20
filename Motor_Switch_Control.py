from Motor_Movement import zplus,zminus,rightstep,leftstep,upwardstep,downwardstep
import RPi.GPIO as GPIO
import time
from os import path
import os.path

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(33,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(29,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
if(path.exists("position_movements.txt")==False):
    f=open("position_movements.txt","w")
    f1=open("present_position.txt","w")
    f.write("0 0\n")
    f1.write("0 0\n")
    f.close();f1.close()
file=open("present_position.txt","r")
curr=file.read()

if(curr==''):
    curr='0 0'
print("tes")
print(curr)
split=curr.split(' ');file.close()
x=float(split[0]);y=float(split[1])

try:
    f=open("position_movements.txt","a")
    cu=open("present_position.txt","w")
    while True:
        if GPIO.input(15):
            zplus()
            time.sleep(0.1)
        if GPIO.input(19):
            zminus()
            time.sleep(0.1)
        if GPIO.input(21):
            ##            if(x-1<0):
            ##                print("moving out of bound on left")
            ##            else:
            x=x-1
            print("x="+str(x)+"y="+str(y))
            f.write(str(x)+" "+str(y)+"\n");cu.seek(0)
            cu.write(str(x)+" "+str(y))
            leftstep()
            time.sleep(0.1)
        if GPIO.input(23):
            ##            if(y-0.126<0):
            ##                print("moving out of bound on down")
            ##            else:
            y=y-1
            print("x="+str(x)+"y="+str(y))
            f.write(str(x)+" "+str(y)+"\n");cu.seek(0)
            cu.write(str(x)+" "+str(y))
            downwardstep()
            time.sleep(0.1)

        if GPIO.input(33):

            ##            if(y+0.126>52):
            ##                print("moving out of bound on up")
            ##            else:
            y=y+1
            print("x="+str(x)+"y="+str(y))
            f.write(str(x)+" "+str(y)+"\n");cu.seek(0)
            cu.write(str(x)+" "+str(y))

            upwardstep()
            time.sleep(0.1)

        if GPIO.input(29):

            ##            if(x+0.126>84):   
            ##                print("moving out of bound on right")
            ##            else:
            x=x+1
            print("x="+str(x)+"y="+str(y))
            f.write(str(x)+" "+str(y)+"\n");cu.seek(0)
            cu.write(str(x)+" "+str(y))
            rightstep()
            time.sleep(0.1)
except KeyboardInterrupt:
    print("KeyBoard has been Interrupted")
except Exception as exc:
    print(exc,"has occured")
finally:
    cu.close()
    f.close()

