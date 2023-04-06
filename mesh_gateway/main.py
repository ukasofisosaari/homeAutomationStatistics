#!/usr/bin/env python3
""" Gateway script for receiving messages from serial port
    and passing them onto MQTT broker.
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

from gateway import MeshGateway


def main():
    """ Main function """
    gateway = MeshGateway()
    gateway.connect_2_mqtt_broker()
    gateway.listen_and_crunch()


if __name__ == "__main__":
    # execute only if run as a script
    main()
