#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import os
import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from binoas.utils import load_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.config['binoas'] = load_config()['binoas']

# Whhopsie, only does for Flask now while we need SQLAlchemy in non-flask too
# need to figure this out tomorrow
db = SQLAlchemy(app)

from app import routes
