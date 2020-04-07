#!/usr/bin/python

#THis script creates a Flask server, and serves the index.html out of the templates folder.
#It also creates an app route to be called via ajax from javascript in the index.html to query
#the database that is being written to by tempReader.py, and return the data as a json object.

#This was written for Joshua Simons's Embedded Linux Class at SUNY New Paltz 2020
#And is licenses under the MIT Software License

#Import libraries as needed
from flask import Flask, render_template, jsonify, Response, request
import sqlite3 as sql
import json
import time
import RPi.GPIO as GPIO

#assign GPIO pins
redPin = 27
greenPin = 22

#LED variables -----------------------------------------------------------
#duration of each blink
blinkDur = .1
#number of times to blink the LED
blinkTime = 7
#-------------------------------------------------------------------------

#initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)


#Globals
app = Flask(__name__)

@app.route("/")
def index():
	print("here")
	return render_template('index.html')

@app.route("/sqlData")
def chartData():
	con = sql.connect('../log/tempLog.db')
	cur = con.cursor()
	con.row_factory = sql.Row
	cur.execute("SELECT Date, Temperature FROM tempLog WHERE Temperature > 60")
	dataset = cur.fetchall()
	print (dataset)
	chartData = []
	for row in dataset:
		chartData.append({"Date": row[0], "Temperature": float(row[1])})
	return Response(json.dumps(chartData), mimetype='application/json')
@app.route("/blinkLight", methods = ['GET','POST'])
def lightUp():
	if request.method == 'POST':
		GPIO.output(22,True)
		time.sleep(blinkDur)
		GPIO.output(22,False)
		time.sleep(blinkDur)
	else:
		GPIO.output(27,True)
		time.sleep(blinkDur)
		GPIO.output(27,False)
		time.sleep(blinkDur)
	return Response(json.dumps('yayaya'), mimetype='application/json')
#	return Response, {'Content-Type': 'text/plain'}
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=2020, debug=True, use_reloader=False)
