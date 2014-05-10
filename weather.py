#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Write some message on the display.
# This project uses https://github.com/dbrgn/RPLCD.
# sudo apt-get install python-matplotlib

from __future__ import print_function, division, absolute_import, unicode_literals

import sys

# Import LCD stuff from RPLCD, et. al.
from RPLCD import CharLCD
from RPLCD import Alignment, CursorMode, ShiftMode
from RPLCD import cursor, cleared

from xml.dom.minidom import *
import urllib
import RPi.GPIO as GPIO
import time
import csv

# Imports for graph plotting
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# some LCD magic happens here
try:
    input = raw_input
except NameError:
    pass

try:
    unichr = unichr
except NameError:
    unichr = chr

# ###################################################################################
# Configure stuff here:
# Temp sensor ID is the folder name for ds18b20 1-wire sensors
# found in /sys/bus/w1/devices/
# Drivers are loaded with
# sudo modprobe w1-gpio
# sudo modprobe w1-therm
# or put them in /etc/modules
TempSensorInside = '28-000005ad1070'
TempSensorOutside = '28-000005ad0691'
# Yahoo location code. Get the right one for your location from Yahoo's weather page.
LocationID = '700029'
# ###################################################################################

# Disable useless GPIO warnings
GPIO.setwarnings(False)

# Start Yahoo weather stuff
# Weather array
# Dimensions: 1 = today, 2 = tomorrow
# Elements: 1 = day, 2 = date, 3 = low temp, 4 = high temp, 5 = weather text
Weatherarray = [["", "", "", "", ""] , ["", "", "", "", ""]]

# Fetch weather XML for Trier, Germany
Trier = urllib.urlopen('http://weather.yahooapis.com/forecastrss?w=' + LocationID + '&u=c').read()

# Parse the XML
Trier = parseString(Trier)

# Get town
Place = Trier.getElementsByTagName('yweather:location')[0]
City = Place.attributes["city"].value
Country = Place.attributes["country"].value

# Get date
Date = Trier.getElementsByTagName('lastBuildDate')[0].firstChild.data

# Get coordinates
Geo_Lat = Trier.getElementsByTagName('geo:lat')[0].firstChild.data
Geo_Long = Trier.getElementsByTagName('geo:long')[0].firstChild.data

# Get today's weather
Today = Trier.getElementsByTagName('yweather:condition')[0]
Weathertext = Today.attributes["text"].value
Temperature = float(Today.attributes["temp"].value)

# Put it all in a list
for Counter in range(2):

    # Weather data for two days
    # Get data
    Future = Trier.getElementsByTagName('yweather:forecast')[Counter]

    # Process data
    Weatherarray[Counter][0] = Future.attributes["day"].value
    Weatherarray[Counter][1] = Future.attributes["date"].value
    Weatherarray[Counter][2] = float(Future.attributes["low"].value)
    Weatherarray[Counter][3] = float(Future.attributes["high"].value)
    Weatherarray[Counter][4] = Future.attributes["text"].value
# End Yahoo weather stuff.

# Start sensor stuff
# The inside sensor
# Open, read, close the sensor files
tempfilein = open("/sys/bus/w1/devices/" + TempSensorInside + "/w1_slave") 

textin = tempfilein.read()

tempfilein.close() 

# Jump to the right position in the sensor file, convert the string to a number, put the decimal point in
secondlinein = textin.split("\n")[1] 
temperaturedatain = secondlinein.split(" ")[9] 
temperaturein = float(temperaturedatain[2:]) 
temperaturein = temperaturein / 1000 
# print temperaturein

# The outside sensor
tempfileout = open("/sys/bus/w1/devices/" + TempSensorOutside + "/w1_slave") 

textout = tempfileout.read() 

tempfileout.close() 

# Jump to the right position in the sensor file, convert the string to a number, put the decimal point in
secondlineout = textout.split("\n")[1] 
temperaturedataout = secondlineout.split(" ")[9] 
temperatureout = float(temperaturedataout[2:]) 
temperatureout = temperatureout / 1000 
# print temperatureout

lcd = CharLCD()


# Print the data onto the display.
lcd.clear()
lcd.write_string(time.strftime("%d.%m.%Y %H:%M"))
lcd.cursor_pos = (1, 0)
#lcd.write_string(str(City) + ' ')
lcd.write_string('Innen:  '+ str(temperaturein) + ' Grad')
lcd.cursor_pos = (2, 0)
lcd.write_string('Aussen: '+ str(temperatureout) + ' Grad')
lcd.cursor_pos = (3, 0)
lcd.write_string(Weathertext)

# Write the data to a webpage on the local server
index = open('/var/www/index.html','w')
index.write(str(City) + ': ' + str(Temperature) + ' C <br> Min: ' + str(Weatherarray[0][2]) + ' C <br> Max: ' + str(Weatherarray[0][3]) + ' C <br>' + Weathertext + '<br><br> Sensordaten: <br> Innen: ' + str(temperaturein) + '<br> Aussen: ' + str(temperatureout) + '<br><br> Updated: ' + time.strftime("%d.%m.%Y %H:%M:%S"))
index.close()


# Write data to a .csv file for graph creation
weather_csv = open('weather.csv', 'a')
datawriter = csv.writer(weather_csv)
datawriter.writerow([time.strftime("%d.%m.%Y %H:%M"),str(temperaturein),str(temperatureout)])
weather_csv.close()

# Read it again and create arrays from it
#weather









