import RPi.GPIO as GPIO
import time

#GPIO setup
channel = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)

def callback(channel):
	if GPIO.input(channel):
		print ("Movement Detected")
	else:
		print ("Movement Detected")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)	#tells when pin goes high or low
GPIO.add_event_callback(channel, callback) 			#assign function to GPIO pin, run function on change

while True:
	time.sleep(1)
