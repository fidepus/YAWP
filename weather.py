#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Write some message on the display.
# This project uses https://github.com/dbrgn/RPLCD.

from __future__ import print_function, division, absolute_import, unicode_literals

import sys

# Import LCD stuff from RPLCD
from RPLCD import CharLCD
from RPLCD import Alignment, CursorMode, ShiftMode
from RPLCD import cursor, cleared

from xml.dom.minidom import *
import urllib

import RPi.GPIO as GPIO

import time

try:
    input = raw_input
except NameError:
    pass

try:
    unichr = unichr
except NameError:
    unichr = chr


# Start Yahoo weather stuff
# Yahoo location code. Get the right one for your location from Yahoo's weather page.
LocationID = '700029'


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


# Disable useless warings
GPIO.setwarnings(False)

lcd = CharLCD()


# Print the data onto the display.
lcd.clear()
lcd.write_string(str(City) + ': ' + str(Temperature) + ' C')
lcd.cursor_pos = (1, 0)
lcd.write_string('Min: ' + str(Weatherarray[0][2]) + ' C')
lcd.cursor_pos = (2, 0)
lcd.write_string('Max: ' + str(Weatherarray[0][3]) + ' C')
lcd.cursor_pos = (3, 0)
lcd.write_string(Weathertext)

# Write the data to a webpage on the local server
index = open('/var/www/index.html','w')
index.write(str(City) + ': ' + str(Temperature) + ' C <br> Min: ' + str(Weatherarray[0][2]) + ' C <br> Max: ' + str(Weatherarray[0][3]) + ' C <br>' + Weathertext + '<br> Updated: ' + time.strftime("%d.%m.%Y %H:%M:%S"))
index.close()
