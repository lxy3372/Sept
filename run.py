#!/usr/bin/env python
# -*-  coding=utf-8 -*-
__author__ = 'Riky'

from application import create_app
from datetime import *
from flask import session
from application.model.db import db

app = create_app('dev')

@app.template_filter('hello')
def reverse_filter(f):
    now = datetime.now()
    date = now.strftime('%p')
    name = session.get(app.config.get('SESSION_KEY'))['nickname']
    return (u"上午好" if date == 'AM' else u"下午好") +u"，"+name

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    else:
        db.session.commit()
    db.session.remove()

app.run()




