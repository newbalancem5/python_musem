
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.IN)

count = 0

# wait for sensor trigger loop
while True:
    print (count)
	# waiting for item
    while GPIO.input(25) == 0:
		time.sleep(0.1)
    count = count + 1
    
    # waiting for item to pass
	while GPIO.input(25) == 1:
		time.sleep(0.1)
		