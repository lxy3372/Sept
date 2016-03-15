#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Ricky'

from flask import render_template, flash, redirect, jsonify
from application.service.UserService import UserService
from application.model.db import DBSession
from application.functions.helper import login_required
from . import main


@main.route('/')
@main.route('/index')
@login_required
def index():
    anything = "asdfsdf"
    return render_template('index.html', option=anything)


@main.route('/about')
def templates(anything=None):
    return "hello world"


@main.route('/login', methods=['GET'])
def login_page():
    return render_template('index.html', option='')


@main.route('/do_login', methods=['GET'])
def do_login():
    errcode, errmsg, data = UserService.login('me@rikyliu.com', '123456')
    return jsonify({'errcode': errcode, 'errmsg': errmsg, 'data': None})


@main.route("/logout")
@login_required
def logout():
    UserService.logout()
    flash("Logged out.")
    return redirect('/login')


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.teardown_app_request
def shutdown_session(exception=None):
    DBSession.remove()

