#!/usr/bin/env python3
"""
    Simple logging module.
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

import logging

from definitions import LOGGING_LEVEL_INFO, LOGGING_LEVEL_DEBUG, \
    LOGGING_LEVEL_ERROR, LOG_LEVEL_DICT


class LoggerPrinter:
    """ Handles all logging and printing for mesh gateway"""
    def __init__(self, log_file, log_level):
        """ Init function"""
        if log_level not in LOG_LEVEL_DICT.keys():
            print(f"Log level: {log_level} not valid: {LOG_LEVEL_DICT}")
        logging.basicConfig(filename=log_file,
                            format='%(asctime)s [%(levelname)s]: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=LOG_LEVEL_DICT[log_level])

    @staticmethod
    def logging_printing(msg, level):
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
