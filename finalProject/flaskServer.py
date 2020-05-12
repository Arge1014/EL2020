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
def index():
    noIntruders = True
    soundDetected = 0
    motionDetected = 0
    vibrationDetected = 0
    try:
        GPIO.setup(pirPin, GPIO.IN)
        GPIO.setup(vibPin, GPIO.IN)
        GPIO.setup(soundPin, GPIO.IN)
    except:
        response = "error reading sensors"
    while noIntruders == True:
        sound = GPIO.input(soundPin)
        vibration = GPIO.input(vibPin)
        motion = GPIO.input(pirPin)
        if sound == 1:
            print("Sound Detected")
            soundDetected = 1
            noIntruders = False
        elif motion == 1:
            print("Motion detected")
            motionDetected = 1
            noIntruders = False
        elif vibration == 1:
            print("Vibration Detected")
            vibrationDetected = 1
            noIntruders = False
        time.sleep(.1)
    templateData = {
        soundDetected,
        motionDetected,
        vibrationDetected
    }
    return render_template('index.html')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)