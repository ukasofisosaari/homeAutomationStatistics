""" This is the gateway script
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

#!/usr/bin/env python3
from time import gmtime, strftime
import configparser
import logging

import socket
import serial
import requests


def post_to_web_server(web_url, query):
    """ Method for posting to web server """
    hostname = socket.gethostname()
    query['hostname'] = hostname
    logging.info(query)

    try:
        res = requests.post(web_url, data=query)
        logging.info(res.text)
    except requests.exceptions.InvalidSchema as request_error:
        print(request_error)
        logging.info(request_error)
    except requests.exceptions.ConnectionError as request_error:
        print(request_error)
        logging.info(request_error)

def main():
    """ Main function """

    config = configparser.ConfigParser()
    config.read('gateway.cfg')
    serial_port = config.get('general', 'SerialPort')
    baudrate = config.get('general', 'Baudrate')
    web_url = config.get('general', 'WebServerURL')
    log_file = config.get('general', 'log_file')
    n_fields_in_msg = config.get('general', 'n_fields_in_msg')


    logging.basicConfig(filename=log_file,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

    try:
        ser = serial.Serial(
            port=serial_port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        logging.info("Serial connection opened")
    except serial.SerialException as error:
        print("No device on serial port: " + serial_port)
        print(error)
        ser = None
        query = {'error_msg' : "No device on serial port: {0}".format(serial_port),
                 'time' : strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        #post_to_web_server(web_url, query)


    #Key is sensor id, value is array of sensor data
    sensors_data_dict = {}

    while 1 and ser:
        try:
            mesh_msg = str(ser.readline()).split(';')
        except serial.serialutil.SerialException:
            exit(2)
            logging.info(mesh_msg)

        if len(mesh_msg) == int(n_fields_in_msg) and mesh_msg[1] == 'R':
            print("Got message")
            logging.info(mesh_msg)
            sensor_data = {}
            for i, value in enumerate(mesh_msg):
                if value == 'R':
                    sensor_data['node_id'] = mesh_msg[i+1]
                elif value == 'H':
                    sensor_data['humidity'] = mesh_msg[i+1]
                elif value == 'T':
                    sensor_data['temperature'] = mesh_msg[i+1]
            sensor_data['time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            try:
                sensors_data_dict[sensor_data['node_id']].append(sensor_data)

                logging.info("Sample number: {0} for sensor {1}",
                             str(len(sensors_data_dict[sensor_data['node_id']])),
                             sensor_data['node_id'])
            except KeyError:
                sensors_data_dict[sensor_data['node_id']] = []
            if len(sensors_data_dict[sensor_data['node_id']]) > 60:
                print("Got 60 samples")
                logging.info("Got 60 samples")
                sensor_data_average = {}
                #Set id and current time
                sensor_data_average['node_id'] = sensor_data['node_id']
                sensor_data_average['time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                temperature_average = 0.0
                humidity_average = 0.0
                for data_sample in sensors_data_dict[sensor_data['node_id']]:
                    temperature_average += float(data_sample['temperature'])
                    humidity_average += float(data_sample['humidity'])
                temperature_average = temperature_average / 60.0
                humidity_average = humidity_average / 60.0
                sensor_data_average['temperature'] = str(temperature_average)
                sensor_data_average['humidity'] = str(humidity_average)
                logging.info(sensor_data_average)
                post_to_web_server(web_url, sensor_data_average)
                sensors_data_dict[sensor_data['node_id']] = []




if __name__ == "__main__":
    # execute only if run as a script
    main()
