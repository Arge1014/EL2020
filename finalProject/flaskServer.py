from flask import Flask, render_template, jsonify, Response, request
import datetime
import time
import json
import smtplib
import RPi.GPIO as GPIO
app = Flask(__name__)

#setting up pins for sensors
pirPin = 17
vibPin = 27
soundPin = 22
buzzerPin = 14
GPIO.setmode(GPIO.BCM)
eFROM = "nickarge1014@gmail.com"
eTO = "9143643339@vtext.com"
Subject = "Intruder Detected"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)


@app.route("/")
def index():
    noIntruders = True
    textSent = False
    soundDetected = 0
    motionDetected = 0
    vibrationDetected = 0
    try:
        GPIO.setup(pirPin, GPIO.IN)
        GPIO.setup(vibPin, GPIO.IN)
        GPIO.setup(soundPin, GPIO.IN)
    except:
        response = "error reading sensors"
    with open("log/detectionlog.csv", "a") as log:
        while noIntruders == True:
            sound = GPIO.input(soundPin)
            vibration = GPIO.input(vibPin)
            motion = GPIO.input(pirPin)
            templateData ={'String' : "No intruders detected"}
            if sound == 1:
                print("Sound Detected")
                soundDetected = 1
                noIntruders = False
                log.write("{0} {1}\n".format(time.strftime("%m-%d-%Y %H:%M:%S"),str("Sound")))
                templateData = {
                    'String': "Sound detected at {0}\n".format(time.strftime("%m-%d-%Y %H:%M:%S"))
                }
                if textSent == False:
                    eMessage = 'Subject: {}\n\n{}'.format(Subject, "Sound detected at {0}\ngo to 10.0.0.53 to set off alarm\n".format(time.strftime("%H:%M:%S")))
                    server.login("nickarge1014@gmail.com", "clguzzwndxwrceqg")
                    server.sendmail(eFROM, eTO, eMessage)
                    textSent = True
            elif motion == 1:
                print("Motion detected")
                motionDetected = 1
                noIntruders = False
                log.write("{0} {1}\n".format(time.strftime("%m-%d-%Y %H:%M:%S"),str("Motion")))
                templateData = {
                    'String': "Motion detected at {0}\n".format(time.strftime("%m-%d-%Y %H:%M:%S"))
                }
                if textSent == False:
                    eMessage = 'Subject: {}\n\n{}'.format(Subject, "Motion detected at {0}\ngo to 10.0.0.53 to set off alarm\n".format(time.strftime("%H:%M:%S")))
                    server.login("nickarge1014@gmail.com", "clguzzwndxwrceqg")
                    server.sendmail(eFROM, eTO, eMessage)
                    textSent = True
            elif vibration == 1:
                print("Vibration Detected")
                vibrationDetected = 1
                noIntruders = False
                log.write("{0} {1}\n".format(time.strftime("%m-%d-%Y %H:%M:%S"),str("Vibration")))
                templateData = {
                    'String': "Vibration detected at {0}\n".format(time.strftime("%m-%d-%Y %H:%M:%S"))
                }
                if textSent == False:
                    eMessage = 'Subject: {}\n\n{}'.format(Subject, "Vibration detected at {0}\ngo to 10.0.0.53 to set off alarm\n".format(time.strftime("%H:%M:%S")))
                    server.login("nickarge1014@gmail.com", "clguzzwndxwrceqg")
                    server.sendmail(eFROM, eTO, eMessage)
                    textSent = True
            time.sleep(.5)
        return render_template('index.html', **templateData)

@app.route("/buzzer", methods = ['GET', 'POST'])
def alarm():
    GPIO.setup(buzzerPin, GPIO.OUT)
    GPIO.output(buzzerPin, False)
    if request.method == 'POST':
        while True:
            GPIO.output(buzzerPin, True)
            return Response(json.dumps('buzzer alarm active'), mimetype='application/json')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)