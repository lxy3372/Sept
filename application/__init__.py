#!/usr/bin/env python
#-*- coding=utf-8 -*-

__author__ = 'Riky'

from flask import Flask
from flask_bootstrap import Bootstrap
from main import main as main_blueprint
from api import api as api_blueprint
from config import config


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    Bootstrap(app)

    return app

