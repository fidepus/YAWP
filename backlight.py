#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Switch the back ligth of a connected LCD on or off, depending on the time
#import RPi.GPIO as GPIO
from datetime import datetime, time
import lcddriver

lcd = lcddriver.lcd()

def switch_light():
	# get the time
	now = datetime.now()
	now_time = now.time()

	# see if it is time to switch on the light
	if now_time >= time(6,00) and now_time <= time(23,00):
	    lcd.backlight(1)
        # if not, switch it off
	else:
		lcd.backlight(0)
