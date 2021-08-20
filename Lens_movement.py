from Motor_Movement import zplus,zminus,rightstep,leftstep,upwardstep,downwardstep
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(33,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(29,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
def hardware_action(x_prev,y_prev,z_prev,x_curr,y_curr,z_curr):
    xsteps=int(x_curr-x_prev)
    ysteps=int(y_curr-y_prev)
    print("goto",x_curr,y_curr)
    print("curr",x_prev,y_prev)
    if(xsteps<0):
        xsteps=-xsteps
        backward(xsteps)
    else:
        forward(xsteps)
    if(ysteps<0):
        ysteps=-ysteps
        downward(ysteps)
    else:
        upward(ysteps)
    


def forward(steps):
    for i in range(0,steps):
        rightstep()
        time.sleep(0.02)
    print("FORWARD MOVEMENT ",steps," STEPS")

def backward(steps):
    for i in range(0,steps):
        leftstep()
        time.sleep(0.02)
    print("BACKWARD MOVEMENT ",steps," STEPS")

def upward(steps):
    for i in range(0,steps):
        upwardstep()
        time.sleep(0.02)
    print("UPWARD MOVEMENT ",steps," STEPS")

def downward(steps):
    for i in range(0,steps):
        downwardstep()
        time.sleep(0.02)
    print("DOWNWARD MOVEMENT ",steps," STEPS")
