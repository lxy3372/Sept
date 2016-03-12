#!/usr/bin/env python
# -*- coding=utf-8 -*-

from functools import wraps
from flask import g,redirect,url_for,request

__author__ = 'Riky'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
    return decorated_function
