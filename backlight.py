#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Switch the back ligth of a connected LCD on or off, depending on the time
import RPi.GPIO as GPIO
from datetime import datetime, time

def switch_light():
	# get the time
	now = datetime.now()
	now_time = now.time()

	# see if it is time to switch on the light
	if now_time >= time(6,00) and now_time <= time(23,00):
	    with open('/home/pi/YAWP/display_light.txt', 'w') as backlight:
	    	backlight.write('1')
	    	light=1
	# if not, switch it off
	else:
		with open('home/pi/YAWP/display_light.txt', 'w') as backlight:
			backlight.write('0')
			light=0

# Pin 11 gives out a "already in use warning". 
# Don't know why, will have to test
	# # Use physical pin numbers
	# GPIO.setmode(GPIO.BOARD)
	# # Set up header pin 11 (GPIO17) as an input
	# print "Setup Pin 11"
	# GPIO.setup(11, GPIO.OUT)
	# # Do the actual switching
	# if light==1:
	# 	GPIO.output(11, True)
	# else:
	# 	GPIO.output(11, False)