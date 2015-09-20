#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Ricky'

from flask import render_template
from . import main


@main.route('/')
def index():
    anything = 'Dota2'
    return render_template('index.html', option=anything)


@main.route('/about')
def templates(anything=None):
    return "hello world"


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
