""" Interactive tool to generate JSON with node_ids of nodes in network
    and their locations
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

#!/usr/bin/env python3
import configparser
import os
import json

from definitions import LOGGING_LEVEL_INFO, LOGGING_LEVEL_DEBUG, LOGGING_LEVEL_ERROR
from definitions import NODE_ID_KEY, TEMPERATURE_KEY, HUMIDITY_KEY
from logger import LoggerPrinter

import serial

class NodeJsonGenerator():
    """ Mesh gateway class, parses mesh network messages
    and publishes them to MQTT broker"""

    def __init__(self):
        """ """
        config = configparser.ConfigParser()
        config.read('gateway.cfg')
        self._serial_port = config.get('general', 'SerialPort')
        self._baudrate = config.get('general', 'Baudrate')

        log_file = config.get('general', 'log_file')
        self._logger = LoggerPrinter(log_file)
        self._nodes = None
        try:
            nodes_file = open("nodes.json")
            self._nodes = json.load(nodes_file)
        except FileNotFoundError:
            self._nodes = {}

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

    def generateJson(self):
        """ Listen on serial connection anc crunches data packages"""
        self._openSerialConnection()
        while 1:
            print("Press enter when you are ready power on new node")
            input()
            print("Power on new node")
            while self._ser:
                try:
                    line = str(self._ser.readline())
                    node_id = self._getNodeId(line)
                    if node_id and node_id not in self._nodes.keys():
                        self._newNode(node_id)
                        print("Are you done with adding new nodes(y/n)")
                        done_with_new_nodes = input()
                        if done_with_new_nodes == 'y':
                            nodes_json_object = json.dumps(self._nodes, indent=4)
                            with open("nodes.json", "w") as jsonfile:
                                jsonfile.write(nodes_json_object)
                            exit()
                        else:
                            break
                except serial.serialutil.SerialException as e:
                    self._logger.loggingPrinting(f"Serial Exception: {e}",
                                    LOGGING_LEVEL_ERROR)


    def _getNodeId(self, line):
        """ Parses node and returns it """
        mesh_msg = line.split(';')
        if len(mesh_msg) > 1 and mesh_msg[1] == 'R':
            self._logger.loggingPrinting(mesh_msg,
                            LOGGING_LEVEL_INFO)
            for i, value in enumerate(mesh_msg):
                if value == 'R':
                    return mesh_msg[i + 1]

    def _newNode(self, node_id):
        """ """
        print(f"New node with id: { node_id } found")
        print("What is the node location")
        while 1:
            location = input()
            print(f"Node location: {location}, confirm(y/n)")
            confirmation = input()
            if confirmation == "y":
                self._nodes[node_id] = location
                break
            else:
                print("Re-enter node location")


def main():
    """ Main function """
    node_json_generator = NodeJsonGenerator()
    node_json_generator.generateJson()

if __name__ == "__main__":
    # execute only if run as a script
    main()