#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import os
import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from binoas.utils import load_config

from flask import Flask, jsonify

from binoas.db import setup_db
from binoas.es import setup_elasticsearch


class BinoasError(Exception):
    """API error class.
    :param msg: the message that should be returned to the API user.
    :param status_code: the HTTP status code of the response
    """

    def __init__(self, msg, status_code):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return repr(self.msg)

    @staticmethod
    def serialize_error(e):
        return jsonify(dict(status='error', error=e.msg)), e.status_code


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['binoas'] = load_config()['binoas']

    app.errorhandler(BinoasError)(BinoasError.serialize_error)

    def add_cors_headers(resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        # See https://stackoverflow.com/questions/12630231/how-do-cors-and-access-control-allow-headers-work
        resp.headers['Access-Control-Allow-Headers'] = 'origin, content-type, accept'
        return resp

    app.after_request(add_cors_headers)

    setup_db(app.config)
    setup_elasticsearch(app.config)

    return app

app = create_app()

from app import routes
