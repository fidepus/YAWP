#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import sys
from xml.dom.minidom import *
import urllib
import RPi.GPIO as GPIO
import time
import csv
import os
import subprocess
import shutil
import decimal
# Import I2C LCD Driver
import lcddriver
# Import Adafruit BMP085 library
from Adafruit_BMP085 import BMP085
import backlight
import humidity
import mqtt

#backlight.switch_light()

# ###################################################################################
# Configure stuff here:
# Temp sensor ID is the folder name for ds18b20 1-wire sensors
# found in /sys/bus/w1/devices/
# Drivers are loaded with
# sudo modprobe w1-gpio
# sudo modprobe w1-therm
# or put them in /etc/modules
Temp_Sensor_Inside = '28-0004441caaff'
Temp_Sensor_Outside = '28-0004441f3aff'
# Yahoo location code. Get the right one for your location from Yahoo's weather page.
Location_ID = '664474'
# Your altitude above sea level in meters.
altitude = 239
# ###################################################################################

# Disable useless GPIO warnings
GPIO.setwarnings(False)

# Temporary fix for Yahoo weather stuff

Weather_Text = 'Feuchte:'
Condition_Code = 'na'

# # Start Yahoo weather stuff
# # Weather array
# # Dimensions: 1 = today, 2 = tomorrow
# # Elements: 1 = day, 2 = date, 3 = low temp, 4 = high temp, 5 = weather text
# Weather_Array = [["", "", "", "", ""] , ["", "", "", "", ""]]

# # Fetch weather XML for Kaiserslautern, Germany
# Kaiserslautern = urllib.urlopen('http://weather.yahooapis.com/forecastrss?w={0}&u=c'.format(Location_ID)).read()

# # Parse the XML
# Kaiserslautern = parseString(Kaiserslautern)

# # Get town
# Place = Kaiserslautern.getElementsByTagName('yweather:location')[0]
# City = Place.attributes["city"].value
# Country = Place.attributes["country"].value

# # Get date
# Date = Kaiserslautern.getElementsByTagName('lastBuildDate')[0].firstChild.data

# # Get coordinates
# Geo_Lat = Kaiserslautern.getElementsByTagName('geo:lat')[0].firstChild.data
# Geo_Long = Kaiserslautern.getElementsByTagName('geo:long')[0].firstChild.data

# # Get today's weather
# Today = Kaiserslautern.getElementsByTagName('yweather:condition')[0]
# Weather_Text = Today.attributes["text"].value
# Temperature = float(Today.attributes["temp"].value)
# Condition_Code = Today.attributes["code"].value

# # Put it all in a list
# for Counter in range(2):

#     # Weather data for two days
#     # Get data
#     Future = Kaiserslautern.getElementsByTagName('yweather:forecast')[Counter]

#     # Process data
#     Weather_Array[Counter][0] = Future.attributes["day"].value
#     Weather_Array[Counter][1] = Future.attributes["date"].value
#     Weather_Array[Counter][2] = float(Future.attributes["low"].value)
#     Weather_Array[Counter][3] = float(Future.attributes["high"].value)
#     Weather_Array[Counter][4] = Future.attributes["text"].value
# # End Yahoo weather stuff.

# Start sensor stuff
# The inside sensor
# Open, read, close the sensor files
with open("/sys/bus/w1/devices/{0}/w1_slave".format(Temp_Sensor_Inside), 'r') as Temp_File_In:
    Text_In = Temp_File_In.read()

# Jump to the right position in the sensor file, convert the string to a number,
# put the decimal point in
Second_Line_In = Text_In.split("\n")[1]
Temperature_Data_In = Second_Line_In.split(" ")[9]
Temperature_In = float(Temperature_Data_In[2:])
Temperature_In = Temperature_In / 1000
# print Temperature_In

# The outside sensor
with open("/sys/bus/w1/devices/{0}/w1_slave".format(Temp_Sensor_Outside), 'r') as Temp_File_Out:
    Text_Out = Temp_File_Out.read()

# Jump to the right position in the sensor file, convert the string to a number,
# put the decimal point in
Second_Line_Out = Text_Out.split("\n")[1]
Temperature_Data_Out = Second_Line_Out.split(" ")[9]
Temperature_Out = float(Temperature_Data_Out[2:])
Temperature_Out = Temperature_Out / 1000
# print Temperature_Out

# Start air pressure stuff
pressure_sensor = BMP085(0x77)
pressure = pressure_sensor.readPressure()
# Altitude correction for pressure at sea level.
psea = pressure / pow(1.0 - altitude/44330.0, 5.255)
psea_dec = psea / 100.0
pressure_relative = decimal.Decimal(psea_dec)
rounded_pressure_relative = pressure_relative.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP)

# Humidty stuff happens here
humidityr = humidity.get_humidity()

##################################
#   LCD stuff happening here     #
##################################

lcd2 = lcddriver.lcd()

backlight.switch_light()
lcd2.lcd_clear()
lcd2.lcd_display_string(time.strftime("%d.%m.%Y %H:%M"), 1)
lcd2.lcd_display_string('Innen: {0} Grad'.format(Temperature_In), 2)
lcd2.lcd_display_string('Aussen: {0} Grad'.format(Temperature_Out), 3)
lcd2.lcd_display_string(str(Weather_Text) + ' ' + str(humidityr) + '%', 4)
backlight.switch_light()

# Write the data to a webpage on the local server
# Get some weather icons that are compliant with Yahoo condition codes.
# The ones by MerlinTheRed are nice and work well
# <http://merlinthered.deviantart.com/art/plain-weather-icons-157162192> CC-BY-NC-SA
with open('/var/www/aktuell.html','w') as index:
    index.write('<style type="text/css">'
        'body {font-weight:lighter; font-family:Arial; font-size:100%; } '
        'h2 {margin:0 0 0 0;} h6 {margin:0 0 0 0;} </style>'
        '<h6>Updated: ' + time.strftime("%d.%m.%Y %H:%M:%S") + '</h6><br><h2>'
        + Weather_Text +
        '</h2><img src="' + Condition_Code + '.png" align="right" alt="Wetter">'
        '<br><br>Innen:<br>'
        '<h2>' + str(Temperature_In) + ' &deg;C</h2><br> Aussen:'
        '<br><h2>' + str(Temperature_Out) + '&deg;C</h2>'
        '<br>Relativer Luftdruck:'
        '<br><h2>' + str(rounded_pressure_relative) + 'hPa</h2>'
        '<br>Luftfeuchtigkeit:'
        '<br><h2>' + str(humidityr) + '%</h2>')

 # Write data to a .csv file for graph creation
with open('/home/pi/YAWP/weather.csv', 'a') as weather_csv:
    Data_Writer = csv.writer(weather_csv)
    Data_Writer.writerow([str(time.strftime('%Y-%m-%d %H:%M')),
        str(Temperature_In),str(Temperature_Out),str('0'),str('15'),
        str(pressure / 100.0), str(rounded_pressure_relative),str(humidityr)])


#send data to mqtt
mqtt.sendmqtt("/members/fidepus/home/livingroom/temperature", Temperature_In)
mqtt.sendmqtt("/members/fidepus/home/outdoor/livingroom", Temperature_Out)
mqtt.sendmqtt("/members/fidepus/home/livingroom/humidity", humidityr)

# From here, a gnuplot file will take over.
# Print graph for one day
p = subprocess.Popen("gnuplot plotter.gpi", shell = True)
os.waitpid(p.pid, 0)
# Print graph for one week
p = subprocess.Popen("gnuplot weekplotter.gpi", shell = True)
os.waitpid(p.pid, 0)
# Print the pressure graph
p = subprocess.Popen("gnuplot pressure.gpi", shell = True)
os.waitpid(p.pid, 0)
# Print the relative pressure graph
p = subprocess.Popen("gnuplot relativepressure.gpi", shell = True)
os.waitpid(p.pid, 0)
# Print the relative pressure graph for one week
p = subprocess.Popen("gnuplot pressureweekplotter.gpi", shell = True)
os.waitpid(p.pid, 0)
# Print the humidity graph for one day
P = subprocess.Popen("gnuplot luftfeuchtigkeit.gpi", shell = True)
#os.waitpid(p.pid, 0)
# Print the humidity graph for one week
#p = subprocess.Popen("gnuplot humidityweekplotter.gpi", shell = True)

# Copy it over to the webserver
shutil.copy2('/home/pi/YAWP/temps.png', '/var/www/')
shutil.copy2('/home/pi/YAWP/weektemps.png', '/var/www/')
shutil.copy2('/home/pi/YAWP/pressure.png', '/var/www/')
shutil.copy2('/home/pi/YAWP/relativepressure.png', '/var/www/')
shutil.copy2('/home/pi/YAWP/relativepressureweek.png', '/var/www/')
shutil.copy2('/home/pi/YAWP/humidity.png', '/var/www/')
shutil.copy2('/home/pi/YAWP/humidityweek.png', '/var/www/')

#backlight.switch_light()

