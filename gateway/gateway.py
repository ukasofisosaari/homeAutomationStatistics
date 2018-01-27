#!/usr/bin/env python 
import time
import serial
import requests


ser = serial.Serial(
  
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
counter=0
url = 'localhost:3001/api/data'

while 1:
    x=ser.readline()
    print x
    query = {'data': x}
    res = requests.post(url, data=query)
    print(res.text)