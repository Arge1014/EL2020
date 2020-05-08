from flask import Flask, render_template
import datetime
import time
import RPi.GPIO as GPIO
app = Flask(__name__)

#setting up pins for sensors
pirPin = 17
vibPin = 27
soundPin = 22
GPIO.setmode(GPIO.BCM)


@app.route("/")
def armed():
    try:
        GPIO.setup(pirPin, GPIO.IN)
        GPIO.setup(vibPin, GPIO.IN)
        GPIO.setup(soundPin, GPIO.IN)
    except:
        response = "error reading sensors"
    GPIO.add_event_detect(pirPin, GPIO.BOTH, bouncetime=300)    #tells if pir is low or high
    GPIO.add_event_callback(pirPin, callback)                   #assign function to GPIO Pin
    GPIO.add_event_detect(vibPin, GPIO.BOTH, bouncetime=300)    #tells if pir is low or high
    GPIO.add_event_callback(vibPin, callback)                   #assign function to GPIO Pin
    GPIO.add_event_detect(soundPin, GPIO.BOTH, bouncetime=300)    #tells if pir is low or high
    GPIO.add_event_callback(soundPin, callback)                   #assign function to GPIO Pin

    while True:
        time.sleep(1)

def callback(channel):
        if GPIO.input(channel):
            print("Intruder Detected")
        else:
            print("intruder detected")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
