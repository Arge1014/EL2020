import RPi.GPIO as GPIO
import time

channel = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
	if GPIO.input(channel):
		print ("Sound Detected")
	else:
		print ("Sound Detected")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)	#tells when pin goes high or low
GPIO.add_event_callback(channel, callback)

while True:
	time.sleep(1)