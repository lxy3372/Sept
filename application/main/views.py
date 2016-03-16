#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Ricky'

from flask import render_template, flash, redirect, jsonify, request, url_for
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
    title = u'登陆'
    return render_template('login.html', option='', title=title)


@main.route('/do_login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']
    flash('ok')
    ret, errmsg, data = UserService.login(email, password)
    return jsonify({'ret': ret, 'errcode': 0, 'errmsg': errmsg, 'data': url_for('main.panel')})


@main.route("/logout")
@login_required
def logout():
    UserService.logout()
    flash("Logged out.")
    return redirect('/login')


@main.route("/admin/panel")
@login_required
def panel():
    title = u'管理后台'
    return render_template('admin/panel.html', option='', title=title)


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.teardown_app_request
def shutdown_session(exception=None):
    DBSession.remove()

