""" Gateway script for receiving messages from serial port
    and passing them onto MQTT broker.
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """
#!/usr/bin/env python3

#Mesh message definitions
NODE_ID_KEY= "node_id"
TEMPERATURE_KEY = "temperature"
HUMIDITY_KEY = "humidity"

#Logging definitions
LOGGING_LEVEL_INFO = 0
LOGGING_LEVEL_DEBUG = 1
LOGGING_LEVEL_ERROR = 2