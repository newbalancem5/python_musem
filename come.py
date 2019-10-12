import time
import RPi.GPIO as GPIO 

def RCtime(RCpin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RCpin, GPIO.IN)
    GPIO.wait_for_edge(RCpin, GPIO.RISING)
    signal = GPIO.input(RCpin)
    try:
        exit()
    except:
        print("Нашелся")

while True:
    RCtime(4)
    time.sleep(2)    
    
        