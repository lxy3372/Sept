#!/usr/bin/env python
#-*- coding=utf-8 -*-

__author__ = 'Ricky'

from flask import Flask
from main import main as main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)

