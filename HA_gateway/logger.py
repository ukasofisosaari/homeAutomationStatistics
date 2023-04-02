"""
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

# !/usr/bin/env python3
import configparser
import logging

from definitions import LOGGING_LEVEL_INFO, LOGGING_LEVEL_DEBUG, LOGGING_LEVEL_ERROR


class LoggerPrinter():
    """ Handles all logging and printing for mesh gateway"""
    def __init__(self):
        """ Init function"""
        config = configparser.ConfigParser()
        config.read('gateway.cfg')
        log_file = config.get('general', 'log_file')

        logging.basicConfig(filename=log_file,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)

    def loggingPrinting(self, msg, level):
        """ Logs to logfile and prints it as well"""
        if level == LOGGING_LEVEL_INFO:
            logging.info(msg)
        elif level == LOGGING_LEVEL_DEBUG:
            logging.debug(msg)
        elif level == LOGGING_LEVEL_ERROR:
            logging.error(msg)
        else:
            pass
        print(msg)
