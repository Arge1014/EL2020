#import libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sys
import smtplib

#assign GPIO pins
redPin = 27
tempPin = 17
greenPin = 22

#eChk = 0
old_time = 60

#temp and humidity sensor
tempSensor = Adafruit_DHT.DHT11

#LED variables -----------------------------------------------------------
#duration of each blink
blinkDur = .1
#number of times to blink the LED
blinkTime = 7
#-------------------------------------------------------------------------

#time between sensor readings
sensorDelay = 60

#email vars
eFROM = "nickarge1014@gmail.com"
eTO = "9143643339@vtext.com"
Subject = "Temperature Warning"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

#initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)

def redBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def greenLight(pin):
	GPIO.output(redPin,False)
	GPIO.output(pin,True)

def readF(tempPin) :
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')
	return tempFahr

def readH(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	if humidity is not None and temperature is not None:
		humid = '{1:0.1f}'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')

	return humid

#def alert(data1):
#	if eChk == 0:

#			Text = "Yo, wats poppin, the temperature is " + str(data1)
#			eMessage = 'Subject: {}\n\n{}'.format(Subject, Text)
#			server.login("nickarge1014@gmail.com", "clguzzwndxwrceqg")
#			server.sendmail(eFROM, eTO, eMessage)
#			server.quit
		#	eChk = 1

#data1 = readF(tempPin)

try:
	with open("../log/tempLogg.csv", "a") as log:

		while True:
#			if 50 <= float(data1) <= 78:
			#	eChk = 0
#				greenLight(greenPin)
#			else:
#				alert(data1)
#				GPIO.output(greenPin, False)
#				redBlink(redPin)

			if time.time() - old_time > 59:
				data1 = readF(tempPin)
				data2 = readH(tempPin)
				print('The Temperature is  '+data1+'*F')
				print('The Humidity is '+data2+'%')
			#	print(eChk)
				log.write("{0},{1},{2}\n".format(time.strftime('%d%H%M'),data1,data2))
				log.flush()
				os.fsync(log)
				time.sleep(.2)
				old_time = time.time()

except KeyboardInterrupt:
	GPIO.cleanup()
