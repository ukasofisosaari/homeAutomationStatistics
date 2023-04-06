#!/usr/bin/env python3
""" Gateway script for receiving messages from serial port
    and passing them onto MQTT broker.
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """


from time import gmtime, strftime, sleep
import socket
import configparser
import json


import serial
import paho.mqtt.client as paho
from paho.mqtt.client import MQTT_ERR_SUCCESS, MQTT_ERR_NO_CONN

from definitions import LOGGING_LEVEL_INFO, LOGGING_LEVEL_DEBUG, LOGGING_LEVEL_ERROR
from definitions import NODE_ID_KEY, PUBLISH_DATATYPE_TOPICS
from logger import LoggerPrinter


class MeshGateway:
    """ Mesh gateway class, parses mesh network messages
    and publishes them to MQTT broker"""

    def __init__(self):
        """ Init """
        config = configparser.ConfigParser()
        config.read('gateway.cfg')
        self._mqtt_broker = config.get('general', 'MqttBroker')
        self._mqtt_port = int(config.get('general', 'MqttPort'))
        self._sampling_count = float(config.get('general', 'SamplingCount'))
        self._serial_port = config.get('general', 'SerialPort')
        self._baud_rate = config.get('general', 'BaudRate')
        # Key is sensor id, value is array of sensor data
        self._sensors_data_dict = {}
        log_file = config.get('general', 'logFile')
        log_level = config.get('general', 'LogLevel')
        self._logger = LoggerPrinter(log_file, log_level)
        self._mqtt_client = None
        self._nodes = None
        try:
            nodes_file = open("nodes.json")
            self._nodes = json.load(nodes_file)
        except FileNotFoundError:
            self._logger.logging_printing(
                "No nodes.json file found, generate it first",
                LOGGING_LEVEL_INFO)
            exit()

    def _open_serial_connection(self):
        """ Open serial connection"""
        try:
            self._ser = serial.Serial(
                port=self._serial_port,
                baudrate=self._baud_rate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            self._logger.logging_printing(
                "Serial connection opened",
                LOGGING_LEVEL_INFO)
        except serial.SerialException as error:
            self._logger.logging_printing(
                f"No device on serial port: {self._serial_port}, error: {error}",
                LOGGING_LEVEL_ERROR)
            self._ser = None

    def listen_and_crunch(self):
        """ Listen on serial connection anc crunches data packages"""
        self._open_serial_connection()
        while 1 and self._ser:
            try:
                line = str(self._ser.readline())
                message_data = self._parse_data_package(line)
                if message_data and len(message_data.keys()) > 0:
                    self._process_data(message_data)
            except serial.serialutil.SerialException as e:
                self._logger.logging_printing(
                    f"Serial Exception: {e}",
                    LOGGING_LEVEL_ERROR)

    def _process_data(self, message_data):
        """ Process Data """
        try:
            self._sensors_data_dict[message_data['node_id']].append(message_data)
            self._logger.logging_printing("Sample number: {0} for sensor {1}".format(
                str(len(self._sensors_data_dict[message_data['node_id']])),
                message_data['node_id']),
                            LOGGING_LEVEL_DEBUG)
        except KeyError:
            self._logger.logging_printing(
                f"Node {message_data['node_id']} located at:"
                f"{self._nodes[message_data['node_id']]} "
                "sent its first package",
                LOGGING_LEVEL_INFO)
            self._sensors_data_dict[message_data['node_id']] = []

        if len(self._sensors_data_dict[message_data['node_id']]) == self._sampling_count:
            sensor_data_average = self._average_sensor_values(message_data['node_id'], self._sensors_data_dict)
            # If mqtt_client is None, this could be used to just collect data. Lots of data.
            if self._mqtt_client:
                self._post_to_mqtt_broker(sensor_data_average)
                self._sensors_data_dict[message_data['node_id']].clear()
                print(self._sensors_data_dict[message_data['node_id']])

    def _parse_data_package(self, line):
        """ Parses data packages gateway receives from mesh"""
        mesh_msg = line.split(';')
        sensor_data = {}
        if len(mesh_msg) > 1 and mesh_msg[1] == 'R':
            self._logger.logging_printing(
                mesh_msg,
                LOGGING_LEVEL_DEBUG)
            for i, value in enumerate(mesh_msg):
                if value == 'R':
                    sensor_data['node_id'] = mesh_msg[i + 1]
                    if sensor_data['node_id'] not in self._nodes:
                        self._logger.logging_printing(
                            f"No location for mesh node {sensor_data['node_id']} found",
                            LOGGING_LEVEL_INFO)
                        self._logger.logging_printing(
                            "Regenerate json and restart gateway service",
                            LOGGING_LEVEL_INFO)
                        return None
                elif value == 'H':
                    sensor_data['humidity'] = mesh_msg[i + 1]
                elif value == 'T':
                    sensor_data['temperature'] = mesh_msg[i + 1]
            sensor_data['time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return sensor_data

    def _average_sensor_values(self, node_id, sensors_data_dict):
        """ Calculates average values for sensor data"""
        self._logger.logging_printing(
            f"Got {self._sampling_count} samples, calculating average",
            LOGGING_LEVEL_DEBUG)
        sensor_data_average = {
            'node_id': node_id,
            'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())
        }

        # Set id and current time

        temperature_average = 0.0
        humidity_average = 0.0
        for data_sample in sensors_data_dict[node_id]:
            temperature_average += float(data_sample['temperature'])
            humidity_average += float(data_sample['humidity'])
        temperature_average = round(temperature_average / self._sampling_count, 2)
        humidity_average = round(humidity_average / self._sampling_count, 2)
        sensor_data_average['temperature'] = str(temperature_average)
        sensor_data_average['humidity'] = str(humidity_average)
        self._logger.logging_printing(
            sensor_data_average,
            LOGGING_LEVEL_DEBUG)
        return sensor_data_average

    def _post_to_mqtt_broker(self, sensor_data_dict):
        """ Method for posting to MQTT broker """
        location = self._nodes[sensor_data_dict[NODE_ID_KEY]]
        for publish_datatype in PUBLISH_DATATYPE_TOPICS.keys():
            if PUBLISH_DATATYPE_TOPICS[publish_datatype] in sensor_data_dict.keys():
                rc, mid = self._mqtt_client.publish(f"hakala/{location}/{publish_datatype}",
                                                    sensor_data_dict[PUBLISH_DATATYPE_TOPICS[publish_datatype]])
                if rc == MQTT_ERR_NO_CONN:
                    self._logger.logging_printing(
                        "No connection MQTT broker",
                        LOGGING_LEVEL_ERROR)
                    self._mqtt_client.disconnect()
                    self.connect_2_mqtt_broker()
                elif rc == MQTT_ERR_SUCCESS:
                    self._logger.logging_printing(
                        f"Published to 'hakala/{location}/{publish_datatype}'",
                        LOGGING_LEVEL_DEBUG)
                else:
                    self._logger.logging_printing(
                        f"Unknown publish rc value {rc}",
                        LOGGING_LEVEL_ERROR)

    def connect_2_mqtt_broker(self):
        """ Handles connecting to MQTT broker"""
        self._mqtt_client = paho.Client("mesh_gateway")
        not_connected = True
        self._logger.logging_printing(
            "Trying to connect to MQTT broker",
            LOGGING_LEVEL_INFO)
        while not_connected:
            try:
                self._mqtt_client.connect(self._mqtt_broker, self._mqtt_port)
                sleep(2)

                print("B")
                not_connected = False
                self._logger.logging_printing(
                    "Connection with MQTT broker made",
                    LOGGING_LEVEL_INFO)
            except ConnectionRefusedError:
                print("A")
                pass
            except socket.timeout:
                print("C")
                pass
