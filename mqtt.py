#!/usr/bin/env python
# -*- coding: utf-8 -*-
# send data to an mqtt broker
import paho.mqtt.client as mqtt

def sendmqtt(topic, message):
    # Define Variables
    MQTT_HOST = "mqtt.starletp9.de"
    MQTT_PORT = 1883
    MQTT_KEEPALIVE_INTERVAL = 45
    MQTT_TOPIC = topic
    MQTT_MSG = message

    #initiate mqtt client
    mqttc = mqtt.Client()

    #connect to broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    #publish message
    mqttc.publish(MQTT_TOPIC,MQTT_MSG, qos=0, retain=True)

    #disconnect from broker
    mqttc.disconnect()
