import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT) # blue

GPIO.setup(17,GPIO.OUT) # yellow
GPIO.setup(7,GPIO.OUT) # red

while(True):
    GPIO.output(2,False)
    GPIO.output(17,False)
    GPIO.output(7,False)
    
    time.sleep(2)
    
    GPIO.output(2,True)
    GPIO.output(17,True)
    GPIO.output(7,True)
    time.sleep(2)
