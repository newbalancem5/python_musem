import time
import RPi.GPIO as GPIO 
import os

def RCtime(RCpin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RCpin, GPIO.IN)
    GPIO.wait_for_edge(RCpin, GPIO.RISING)
    signal = GPIO.input(RCpin)
while True:
    RCtime(4)
    time.sleep(2)    
    os.system("omxplayer -o local mvd.mp4")
      