# -*- coding: utf-8 -*-

"""
ivolve_cloud7_logger.core
~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the basic interfaces for our log-metrics package.
"""

import os
import requests
import json
from Cryptodome.Cipher import AES
from Cryptodome import Random

SERVICE_IP = os.environ.get('MS_LOGGER_IP')
SERVICE_PORT = os.environ.get('MS_LOGGER_PORT')
SECRET_KEY = os.getenv('MS_LOGGER_SECRET_KEY', '')
LOG_TARGET = os.getenv('LOG_TARGET', 'console')
endpoint = "http://"+SERVICE_IP+":"+SERVICE_PORT+"/log/python"

MS_NAME = os.getenv('MS_LOGGER_THIS_SERVICE_NAME', 'other')
MS_IP = os.getenv('MS_LOGGER_THIS_SERVICE_IP', '0.0.0.0')
MS_PORT = os.getenv('MS_LOGGER_THIS_SERVICE_PORT', '8000')

ENABLED = True if (SERVICE_IP and SECRET_KEY) else False
CHECK = True if (LOG_TARGET == 'console' or LOG_TARGET == 'both') else False

log = {
    'service': '',
    'IP': '',
    'port': '',
    'type': '',
    'message': '',
}

if (ENABLED and CHECK):
    print('[INFO] logger service started.')


class Console:
    @staticmethod
    def log(*d):
        checkLog(d, 'log', '[LOG]')

    @staticmethod
    def error(*d):
        checkLog(d, 'error', '[ERROR]')

    @staticmethod
    def warn(*d):
        checkLog(d, 'warning', '[WARN]')

    @staticmethod
    def exception(*d):
        checkLog(d, 'exception', '[EXCEPTION]')


def checkLog(d, type_, quote):
    if (LOG_TARGET == 'both'):
        addConsoleLog(d, type_, quote)
        sendLog(d, type_)
    elif (LOG_TARGET == 'kibana'):
        sendLog(d, type_)
    elif (LOG_TARGET == 'console'):
        addConsoleLog(d, type_, quote)


def addConsoleLog(d, type_, quote):
    if (type_ == 'log'):
        print(quote, d)
    elif (type_ == 'error'):
        print(quote, d)
    elif (type_ == 'warning'):
        print(quote, d)
    elif(type_ == 'exception'):
        print(quote, d)


def sendLog(data, type_):
    log["service"] = MS_NAME
    log["ip"] = MS_IP
    log["port"] = MS_PORT
    log["type"] = type_
    log["message"] = str(data)
    try:
        sendToLogstash(log)
    except Exception as error:
        print(error)


def sendToLogstash(data):
    if (ENABLED):
        try:
            headers = { 'secret-key': SECRET_KEY }
            requests.post(endpoint, data=data, headers=headers)
        except Exception as e:
            print(e)


def encrypt(data):
    raw = ''
    length = 16 - (len(data) % 16)
    raw += bytes([length])*length
    key = '12345678901234561234567890123456'
    iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)