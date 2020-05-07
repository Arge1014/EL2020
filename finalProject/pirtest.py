import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)		#Read from motion sensor
GPIO.setup(3, GPIO.OUT)		#LED output pin

#looking for motion
while True:
	i=GPIO.input(11)
	if i==0:
		print ("No Intruders", i)
		GPIO.output(3, 0)
		time.sleep(2)
	elif i==1:
		print ("intruder detected!", i)
		GPIO.output(3, 1)
		time.sleep(2)
