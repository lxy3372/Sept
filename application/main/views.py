#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Ricky'

from flask import render_template
from . import main
from application.service.UserService import UserService
from application.model.db import DBSession
from application.service import decorate


@main.route('/')
def index():
    r = UserService.login('me@rikyliu.com', '123456')
    anything = r.email
    return render_template('index.html', option=anything)


@main.route('/about')
@decorate.login_required
def templates(anything=None):
    return "hello world"


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.teardown_app_request
def shutdown_session(exception=None):
    DBSession.remove()

