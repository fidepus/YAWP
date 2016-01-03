#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Read the data from a AM2302 sensor
import Adafruit_DHT

def get_humidity():

	sensor = Adafruit_DHT.AM2302
	pin = 27

	long_humidity, temp = Adafruit_DHT.read_retry(sensor, pin)

	humidity = round (long_humidity, 3)
	return humidity