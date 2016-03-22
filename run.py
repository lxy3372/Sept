#!/usr/bin/env python
# -*-  coding=utf-8 -*-

from application import create_app
from datetime import *
from flask import session, jsonify, render_template
from application.model.db import db

__author__ = 'Riky'

app = create_app('dev')




app.run()
