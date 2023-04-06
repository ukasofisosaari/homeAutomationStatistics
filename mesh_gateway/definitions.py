#!/usr/bin/env python3
""" Gateway definitions.
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

import logging

# Mesh message definitions
NODE_ID_KEY = "node_id"
TEMPERATURE_KEY = "temperature"
HUMIDITY_KEY = "humidity"
AIR_PRESSURE_KEY = "humidity"

# MQTT publish data types
PUBLISH_TOPIC_TEMPERATURE = "temp"
PUBLISH_TOPIC_HUMIDITY = "hum"
PUBLISH_TOPIC_AIR_PRESSURE = "air_p"

PUBLISH_DATATYPE_TOPICS = {
    PUBLISH_TOPIC_HUMIDITY: HUMIDITY_KEY,
    PUBLISH_TOPIC_TEMPERATURE: TEMPERATURE_KEY,
    PUBLISH_TOPIC_AIR_PRESSURE: AIR_PRESSURE_KEY
}

# Logging definitions
LOGGING_LEVEL_INFO = 0
LOGGING_LEVEL_DEBUG = 1
LOGGING_LEVEL_ERROR = 2

LOG_LEVEL_DICT = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR
}
