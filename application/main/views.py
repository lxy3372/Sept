#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Ricky'

from flask import render_template, flash, redirect, jsonify, request, url_for
from application.service.UserService import UserService
from application.functions.helper import login_required, get_title_by_func, templated
from application.model.db import db
from . import main



@main.route('/')
@main.route('/index')
@login_required
@templated(template='index.html')
def index():
    title = get_title_by_func(index.func_name)
    anything = "asdfsdf"
    return render_template('index.html', option=anything, title=title)


@main.route('/about')
def templates(anything=None):
    return "hello world"


@main.route('/login', methods=['GET'])
@templated(template='login.html')
def login_page():
    title = get_title_by_func(login_page.func_name)
    return dict(option='', title=title)


@main.route('/do_login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']
    flash('ok')
    ret, errmsg, data = UserService.login(email, password)
    return jsonify({'ret': ret, 'errcode': 0, 'errmsg': errmsg, 'data': url_for('admin.panel')})


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
    pass

