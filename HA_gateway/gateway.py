""" Gateway script for receiving messages from serial port
    and passing them onto MQTT broker.
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

#!/usr/bin/env python3
from time import gmtime, strftime, sleep
import socket
import configparser


import serial
import paho.mqtt.client as paho
from paho.mqtt.client import MQTT_ERR_SUCCESS, MQTT_ERR_NO_CONN

from definitions import LOGGING_LEVEL_INFO, LOGGING_LEVEL_DEBUG, LOGGING_LEVEL_ERROR
from definitions import NODE_ID_KEY, TEMPERATURE_KEY, HUMIDITY_KEY
from logger import LoggerPrinter

# Key is node id, value is location.
# TODO: support setting this on the run.
OBJECTS = {"3943546298" : "pirtti", "572294245" : "sauna"}

class MeshGateway():
    """ Mesh gateway class, parses mesh network messages
    and publishes them to MQTT broker"""

    def __init__(self):
        """ """
        config = configparser.ConfigParser()
        config.read('gateway.cfg')
        self._mqtt_broker = config.get('general', 'MqttBroker')
        self._mqtt_port = int(config.get('general', 'MqttPort'))
        self._n_samples = float(config.get('general', 'Samples'))
        self._serial_port = config.get('general', 'SerialPort')
        self._baudrate = config.get('general', 'Baudrate')
        # Key is sensor id, value is array of sensor data
        self._sensors_data_dict = {}
        self._logger = LoggerPrinter()

    def _openSerialConnection(self):
        """ Open serial connection"""
        try:
            self._ser = serial.Serial(
                port=self._serial_port,
                baudrate=self._baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            self._logger.loggingPrinting("Serial connection opened",
                            LOGGING_LEVEL_INFO)
        except serial.SerialException as error:
            self._logger.loggingPrinting(
                f"No device on serial port: {self._serial_port}, error: {error}",
                LOGGING_LEVEL_ERROR)
            self._ser = None

    def listenAndCrunch(self):
        """ Listen on serial connection anc crunches data packages"""
        self._openSerialConnection()
        while 1 and self._ser:
            try:
                line = str(self._ser.readline())
            except serial.serialutil.SerialException:
                exit(2)
                self._logger.loggingPrinting(line,
                                LOGGING_LEVEL_ERROR)
            message_data = self._parse_data_package(line)
            if len(message_data.keys()) > 0:
                self._processData(message_data)


    def _processData(self, message_data):
        """ """
        try:
            self._sensors_data_dict[message_data['node_id']].append(message_data)
            self._logger.loggingPrinting("Sample number: {0} for sensor {1}".format(
                str(len(self._sensors_data_dict[message_data['node_id']])),
                message_data['node_id']),
                            LOGGING_LEVEL_INFO)
        except KeyError:
            self._sensors_data_dict[message_data['node_id']] = []

        if len(self._sensors_data_dict[message_data['node_id']]) == self._n_samples:
            sensor_data_average = self._averageSensorValues(message_data['node_id'],
                                                            self._sensors_data_dict)
            self._post_to_mqtt_broker( sensor_data_average)
            self._sensors_data_dict[message_data['node_id']].clear()
            print(self._sensors_data_dict[message_data['node_id']])

    def _parse_data_package(self, line):
        """ Parses data packages gateway receives from mesh"""
        mesh_msg = line.split(';')
        sensor_data = {}
        if len(mesh_msg) > 1 and mesh_msg[1] == 'R':
            self._logger.loggingPrinting(mesh_msg,
                            LOGGING_LEVEL_INFO)
            for i, value in enumerate(mesh_msg):
                if value == 'R':
                    sensor_data['node_id'] = mesh_msg[i + 1]
                elif value == 'H':
                    sensor_data['humidity'] = mesh_msg[i + 1]
                elif value == 'T':
                    sensor_data['temperature'] = mesh_msg[i + 1]
            sensor_data['time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return sensor_data

    def _averageSensorValues(self, node_id, sensors_data_dict):
        """ Calculates average values for sensor data"""
        self._logger.loggingPrinting(
            f"Got {self._n_samples} samples, calculating average",
                        LOGGING_LEVEL_INFO)
        sensor_data_average = {}

        # Set id and current time
        sensor_data_average['node_id'] = node_id
        sensor_data_average['time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        temperature_average = 0.0
        humidity_average = 0.0
        for data_sample in sensors_data_dict[node_id]:
            temperature_average += float(data_sample['temperature'])
            humidity_average += float(data_sample['humidity'])
        temperature_average = temperature_average / self._n_samples
        humidity_average = humidity_average / self._n_samples
        sensor_data_average['temperature'] = str(temperature_average)
        sensor_data_average['humidity'] = str(humidity_average)
        self._logger.loggingPrinting(sensor_data_average,
                        LOGGING_LEVEL_INFO)
        return sensor_data_average

    def _post_to_mqtt_broker(self, sensor_data_dict):
        """ Method for posting to MQTT broker """
        try:
            location = OBJECTS[sensor_data_dict[NODE_ID_KEY]]
        except KeyError:
            # TODO: Add to objects somehow
            pass
        try:
            rc, mid = self._mqtt_client.publish(f"hakala/{location}/temp",
                                          sensor_data_dict[TEMPERATURE_KEY])
            if rc == MQTT_ERR_NO_CONN:
                # TODO: Reconnect
                self._logger.loggingPrinting(
                    "No connection MQTT broker",
                    LOGGING_LEVEL_ERROR)
                self._mqtt_client.disconnect()
                self._mqtt_client = self.connect2MQTTBroker()
            elif rc == MQTT_ERR_SUCCESS:
                self._logger.loggingPrinting(
                    f"Published to 'hakala/{location}/temp'",
                    LOGGING_LEVEL_DEBUG)
            else:
                self._logger.loggingPrinting(f"Unkown publish rc value {rc}",
                                LOGGING_LEVEL_INFO)

        except KeyError:
            pass

        try:
            rc, mid = self._mqtt_client.publish(f"hakala/{location}/hum",
                                          sensor_data_dict[HUMIDITY_KEY])
            if rc == MQTT_ERR_NO_CONN:
                self._logger.loggingPrinting("No connection MQTT broker", LOGGING_LEVEL_ERROR)
                self._mqtt_client.disconnect()
                mqtt_client = self.connect2MQTTBroker()
            elif rc == MQTT_ERR_SUCCESS:
                self._logger.loggingPrinting(f"Published to 'hakala/{location}/hum'",
                                LOGGING_LEVEL_DEBUG)
            else:
                self._logger.loggingPrinting(f"Unkown publish rc value {rc}",
                                LOGGING_LEVEL_INFO)
        except KeyError:
            pass

    def connect2MQTTBroker(self):
        """ Handles connecting to MQTT broker"""
        self._mqtt_client = paho.Client("mesh_gateway")
        not_connected = True
        self._logger.loggingPrinting("Trying to connect to MQTT broker",
                        LOGGING_LEVEL_INFO)
        while not_connected:
            try:
                self._mqtt_client.connect(self._mqtt_broker, self._mqtt_port)
                sleep(2)

                print("B")
                not_connected = False
                self._logger.loggingPrinting("Connection with MQTT broker made",
                                LOGGING_LEVEL_INFO)
            except ConnectionRefusedError:
                print("A")
                pass
            except socket.timeout:
                print("C")
                pass

def main():
    """ Main function """
    gateway = MeshGateway()
    gateway.connect2MQTTBroker()
    gateway.listenAndCrunch()

if __name__ == "__main__":
    # execute only if run as a script
    main()
