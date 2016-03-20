#!/usr/bin/env python
# -*- coding=utf-8 -*-

from sqlalchemy import Column, Integer, String
from application.model.db import db

__author__ = 'Riky'


class User(db.Model):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(32))
    pic = Column(String(100))
    is_active = Column(Integer)

    def __init__(self, nickname=None, email=None, password=None, pic=None, is_active=1):
        self.nickname = nickname
        self.email = email
        self.password = password
        self.pic = pic
        self.is_active = is_active

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


