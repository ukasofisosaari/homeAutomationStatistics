""" Gateway script for receiving messages from serial port
    and passing them onto MQTT broker.
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """
#!/usr/bin/env python3
import logging

#Mesh message definitions
NODE_ID_KEY= "node_id"
TEMPERATURE_KEY = "temperature"
HUMIDITY_KEY = "humidity"
AIR_PRESSURE_KEY = "humidity"

#MQTT publish datatypes
PUBLISH_TOPIC_TEMPERATURE = "temp"
PUBLISH_TOPIC_HUMIDITY = "hum"
PUBLISH_TOPIC_AIR_PRESSURE = "airp"

PUBLISH_DATATYPE_TOPICS = { PUBLISH_TOPIC_HUMIDITY: HUMIDITY_KEY,
                            PUBLISH_TOPIC_TEMPERATURE: TEMPERATURE_KEY,
                            PUBLISH_TOPIC_AIR_PRESSURE: AIR_PRESSURE_KEY}

#Logging definitions
LOGGING_LEVEL_INFO = 0
LOGGING_LEVEL_DEBUG = 1
LOGGING_LEVEL_ERROR = 2

LOG_LEVEL_DICT = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR
}