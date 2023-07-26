import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
# dibawah pin tx rx
# GPIO.setup(18,GPIO.IN)
def read_depth(pin):
    global start,jarak,end,t
    const = 34000
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)
    # time.sleep(0.000002)
    time.sleep(0.0002)

    GPIO.output(pin,1)
    # time.sleep(0.000005)
    time.sleep(0.0005)

    GPIO.output(pin,0)
    GPIO.setup(pin,GPIO.IN)
    
    while GPIO.input(pin)==0:
        start = time.time()
    while GPIO.input(pin)==1:
        end = time.time()
    t = end-start
    jarak = t*(const/2)
    return jarak
# while True:

#     print(read_depth(18))
