#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Ricky'

from flask import render_template
from . import main

@main.route('/')
def index():
    return "hello world"

@main.route('/about')
@main.route('/about/<anything>')
def templates(anything=None):
    return render_template('about.html', option=anything)


@main.errorhandler(404)
def page_not_found(e):
    pass
