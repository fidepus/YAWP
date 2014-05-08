#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Write some message on the display.
# This project uses https://github.com/dbrgn/RPLCD.

from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from RPLCD import CharLCD
from RPLCD import Alignment, CursorMode, ShiftMode
from RPLCD import cursor, cleared

from xml.dom.minidom import *
import urllib

import RPi.GPIO as GPIO

try:
    input = raw_input
except NameError:
    pass

try:
    unichr = unichr
except NameError:
    unichr = chr

# Weather array
# 1. Dimension = heute, 2. Dimension = naechster Tag
# 1. Element = Tag, 2. Element = Datum, 3. = Niedrigste Temperatur, 4. Element = Hoechste Temperatur, 5. Element = Wettersituation
Weather = [["", "", "", "", ""] , ["", "", "", "", ""]]

# Fetch weather XML for Trier, Germany
Trier = urllib.urlopen('http://weather.yahooapis.com/forecastrss?w=700029&u=c').read()

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

# Get weather text
Weathertext = Today.attributes["text"].value

# Get temperature
Temperature = float(Today.attributes["temp"].value)

# Put it all in a list
for Counter in range(2):

    # Weather data for two days
    # Get data
    Future = Trier.getElementsByTagName('yweather:forecast')[Counter]

    # Process data
    Weather[Counter][0] = Future.attributes["day"].value
    Weather[Counter][1] = Future.attributes["date"].value
    Weather[Counter][2] = float(Future.attributes["low"].value)
    Weather[Counter][3] = float(Future.attributes["high"].value)
    Weather[Counter][4] = Future.attributes["text"].value


# Disable useless warings
GPIO.setwarnings(False)

lcd = CharLCD()

lcd.clear()
lcd.write_string(str(City) + ': ' + str(Temperature) + ' C')
lcd.cursor_pos = (1, 0)
lcd.write_string('Min: ' + str(Weather[0][2]) + ' C')
lcd.cursor_pos = (2, 0)
lcd.write_string('Max: ' + str(Weather[0][3]) + ' C')
lcd.cursor_pos = (3, 0)
lcd.write_string(Weathertext)
