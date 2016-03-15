#!/usr/bin/env python
# -*- coding=utf-8 -*-

from functools import wraps
from flask import redirect, session, current_app, flash

__author__ = 'Riky'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get(current_app.config.get('SESSION_KEY')):
            flash(u'没有登陆')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
