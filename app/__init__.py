#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import os
import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
