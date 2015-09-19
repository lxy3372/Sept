#!/usr/bin/env python
#-*- coding=utf-8 -*-

__author__ = 'Riky'

from flask import Flask
from flask_bootstrap import Bootstrap
from main import main as main_blueprint


def create_app(conifg = None):
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    Bootstrap(app)

    return app

