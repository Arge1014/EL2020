#import libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os

#assign GPIO pins
redPin = 27
tempPin = 17
buttonPin = 26

#temp and humidity sensor
tempSensor = Adafruit_DHT.DHT11

#LED variables -----------------------------------------------------------
#duration of each blink
blinkDur = .1
#number of times to blink the LED
blinkTime = 7
#-------------------------------------------------------------------------

#initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readF(tempPin) :
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}*F'.format(temperature)
		hum = '{1:0.1f}%'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')
	return tempFahr,hum

try:
	with open("../log/tempLog.csv", "a") as log:

		while True:
			input_state = GPIO.input(buttonPin)
			if input_state == False:
				for i in range(blinkTime):
					oneBlink(redPin)
				time.sleep(60)
			data = readF(tempPin)
			print (data)
			log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(data)))

except KeyboardInterrupt:
	GPIO.cleanup()
