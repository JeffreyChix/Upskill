'''
 ********    UPSKILL PROJECT    **********
Weather Detection System to get real-time weather metrics live onto moblie notifications

>>> BRIEF DESCRIPTION OF THE PROJECT 

This project is basically a system designed and programmed with raspberry pi( a computer itself)
and a sensor called SENSE HAT used to detect and measure temperature and humidity readings from an
environment. The readings are displayed on the screen, stored in a file and are sent as notifications to a smartphone. Stay tuned!

CHALLENGES AND MODIFICATIONS

Designing such a project virtually was a little bit impossible because the Frizting app that was meant to 
be used lacked the sensor to read the temperature and humidity. So there was no way to produce the schematics. It
could have been better if it was physically made.

Moreover, I couldn't install the Rasbian operating system for the raspberry PI. So I wrote the program
with an editor and it should run pretty well when uploaded to the computer (Raspberry PI)

Please note that I developed this code with the help of Euderka IOT tutorials for beginners. You can 
find out more on YouTube.
'''
#Import the libraries needed for this project
import pycurl, json
from StringIO import StringIO
import RPi.GPIO as GPIO

from sense_hat import SenseHat
import time
from time import asctime

sense = SenseHat()
sense.clear()

cold = 37 #threshold cold temperature
hot = 40  #threshold hot temperature
pushMessage = "" #this will hold some important message 

OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS = [1,1,1,1,0,1,1,0,1,1,0,1,1,1,1, #0
        0,1,0,0,1,0,0,1,0,0,1,0,0,1,0, #1
        1,1,1,0,0,1,0,1,0,1,0,0,1,1,1, #2
        1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, #3
        1,0,0,1,0,1,1,1,1,0,0,1,0,0,1, #4
        1,1,1,1,0,0,1,1,1,0,0,1,1,1,1, #5
        1,1,1,1,0,0,1,1,1,1,0,1,1,1,1, #6
        1,1,1,0,0,1,0,1,0,1,0,0,1,0,0, #7
        1,1,1,1,0,1,1,1,1,1,0,1,1,1,1, #8
        1,1,1,1,0,1,1,1,1,0,0,1,0,0,1] #9

 #displays a single digit from 0-9      
 def show_digit(val, xd, yd, r, g, b):
 	offset = val * 15
 	for p in range(offset, offset + 15):
 		xt = p % 3
 		yt = (p-offset) // 3
 		sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])
#displays on the screen a two digit positive number 0-99
def show_number(val, r, g, b):
	abs_val = abs(val)
	tens = abs_val // 10
	units = abs_val % 10
	if (abs_val > 9): show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
	show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)

temp = round(sense.get_temperature())
humidity = round(sense.get_humidity())
pressure = round(sense.get_pressure())
message = ' T=%dC, H=%d , P=%d' %(temp,humidity,pressure)

'''
Instapush is an online platform where you can create events for your IOT projects. 
Our system will communicate data to and fro in order to keep track of what's happening and 
send us notifications on our smart phone (the user's smartphone)
'''


appID = "Enter the application id from instapush" # this is available when an account is created with instapush
appSecret = "Enter the application secret from instapush" #also available from instapush

pushEvent = "Enter your event name" #enter the event name you created

c = pycurl.Curl()

c.setopt(c.URL, "instapush url")
c.setopt(c.HTTPHEADER, ['x-instapush-appid: '+ appID + 
						'x-instapush-appsecret: ' + appSecret +  
						'Content-type: application/json'])

buffer = StringIO()

def p(pushMessage):
	json_fields = {}
	json_fields['event'] = pushEvent
	json_fields['trackers'] = {}
	json_fields['trackers']['message'] = pushMessage
	post_fields = json.dump(json_fields)

	c.setopt(c.POSTFIELDS, postfields) 
	c.setopt(c.WRITEFUNCTION, buffer.write)

	c.setopt(c.VERBOSE, True)

while True:
	temp = round(sense.get_temperature())
	humidity = round(sense.get_humidity())
	pressure = round(sense.get_pressure())
	message = ' T=%dC, H=%d , P=%d' %(temp,humidity,pressure)
	time.sleep(4)
	log = open('weather.txt', "a")
	now = str(asctime())
	temp = int(temp)
	show_number(temp, 200, 0, 60)
	temp1 = temp

	log.write(now+' '+message+'\n')
	print(message)
	log.close()
	time.sleep(5)

	if temp >= hot:
		pushMessage = "Its hot: " + message
		p(pushMessage)
		c.perform()
		body = buffer.getvalue()
		pushMessage = ""

	elif temp <= cold:
		pushMessage = "Its cold: " + message
		p(pushMessage)
		c.perform()
		body = buffer.getvalue()
		pushMessage = "" 


	buffer.truncate(0)
	buffer.seek(0)

c.close()
GPIO.cleanup()








