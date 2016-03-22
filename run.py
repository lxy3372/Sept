#!/usr/bin/env python
# -*-  coding=utf-8 -*-

from application import create_app
from datetime import *
from flask import session, jsonify, render_template
from application.model.db import db
from application.functions.helper import InvalidUsage

__author__ = 'Riky'

app = create_app('dev')


@app.template_filter('hello')
def reverse_filter(f):
    now = datetime.now()
    date = now.strftime('%p')
    name = session.get(app.config.get('SESSION_KEY'))['nickname']
    return (u"上午好" if date == 'AM' else u"下午好") + u"，" + name


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    else:
        db.session.commit()
    db.session.remove()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.run()
