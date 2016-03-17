#!/usr/bin/env python
# -*- coding=utf-8 -*-

from sqlalchemy import Column, Integer, String
from db import BaseModel
from db import DBSession

__author__ = 'Riky'


class User(BaseModel):
    __tablename__ = 't_user'

    query = DBSession.query_property()

    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(32))
    pic = Column(String(100))

    def __init__(self, nickname=None, email=None, password=None, pic=None):
        self.nickname = nickname
        self.email = email
        self.password = password
        self.pic = pic

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


