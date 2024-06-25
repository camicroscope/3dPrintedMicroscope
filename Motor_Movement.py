import time


def is_running_on_pi():
    try:
        with open('/proc/device-tree/model') as f:
            model = f.read()
        return 'Raspberry Pi' in model
    except Exception:
        return False

if is_running_on_pi():
    import RPi.GPIO as GPIO
else:
    import FakeGPIO as GPIO
    

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW) # Dir pin 3 of shield x- dir motor
GPIO.setup(18,GPIO.OUT,initial=GPIO.LOW) # Step Pin 6 of shield 
GPIO.setup(22,GPIO.OUT,initial=GPIO.LOW) # Dir pin 4 of shield y-dir motor
GPIO.setup(24,GPIO.OUT,initial=GPIO.LOW) # Step pin 7 of shield

GPIO.setup(11,GPIO.OUT,initial=GPIO.HIGH)#Enable bar pin 8 of shield => Initially the motor is not enabled
GPIO.setup(13,GPIO.OUT,initial=GPIO.LOW) #Dir pin 2 of shield
GPIO.setup(31,GPIO.OUT,initial=GPIO.LOW) #Step pin 5 of shield

def zplus():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.LOW)
    for i in range(0,1):
        GPIO.output(31,GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(31,GPIO.LOW)
        time.sleep(0.02)
    print("ZPLUS")
    GPIO.output(11,GPIO.HIGH)

def zminus():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    for i in range(0,1):
        GPIO.output(31,GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(31,GPIO.LOW)
        time.sleep(0.02)
    print("ZMINUS")
    GPIO.output(11,GPIO.HIGH)

    
def rightstep():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    for i in range(0,1):
        GPIO.output(18,GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(18,GPIO.LOW)
        time.sleep(0.02)
    print("RIGHT")
    GPIO.output(11,GPIO.HIGH)

  
def leftstep():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(16,GPIO.HIGH)
    for i in range(0,1):
        GPIO.output(18,GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(18,GPIO.LOW)
        time.sleep(0.02)
    print("LEFT")
    GPIO.output(11,GPIO.HIGH)

   
def upwardstep():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(22,GPIO.LOW)
    for i in range(0,1):
        GPIO.output(24,GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(24,GPIO.LOW)
        time.sleep(0.02)
    print("UPWARD")
    GPIO.output(11,GPIO.HIGH)


def downwardstep():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(22,GPIO.HIGH)
    for i in range(0,1):
        GPIO.output(24,GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(24,GPIO.LOW)
        time.sleep(0.02)
    print("DOWNWARD")
    GPIO.output(11,GPIO.HIGH)
    
