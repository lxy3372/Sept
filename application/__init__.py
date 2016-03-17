#!/usr/bin/env python
# -*- coding=utf-8 -*-


from flask import Flask
from flask_bootstrap import Bootstrap
from main import main as main_blueprint
from admin import admin as admin_blueprint
from config import config

__author__ = 'Riky'

blueprints = [
    'main_blueprint',
    'api_blueprint'
]


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    Bootstrap(app)

    return app
