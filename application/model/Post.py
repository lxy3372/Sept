#!/usr/bin/env python
# -*- coding=utf-8 -*-

from sqlalchemy import Column
from application.model.db import db
from datetime import datetime

__author__ = 'Riky'


class Post(db.Model):
    """
    POST model
    """

    __tablename__ = 't_post'

    post_id = Column(db.Integer, primary_key=True)
    post_title = Column(db.String(100))
    post_content = Column(db.Text)
    post_type = Column(db.Integer)
    user_id = Column(db.Integer)
    post_tag_id_str = Column(db.String(100))
    post_pic_id_str = Column(db.String(100))
    create_time = Column(db.DateTime)
    update_time = Column(db.DateTime)
    is_active = Column(db.Integer)
    post_seo = Column(db.String(255))

    def __init__(self, title, content, type, user_id, post_tag_id_str=None, post_pic_id_str=None, is_active=1,
                 seo=None):
        self.post_title = title
        self.post_content = content
        self.post_type = type
        self.user_id = user_id
        self.post_tag_id_str = post_tag_id_str
        self.post_pic_id_str = post_pic_id_str
        self.is_active = is_active
        self.post_seo = seo
        self.create_time = datetime.utcnow()
        self.update_time = datetime.utcnow()

    def __repr__(self):
        return '<Post %r>' % (self.post_title)

    def get_id(self):
        return unicode(self.pic_id)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class Tag(db.Model):
    """
    tag model
    """
    __tablename__ = 't_tag'

    tag_id = Column(db.Integer, primary_key=True)
    tag_name = Column(db.String(100), unique=True)
    create_time = Column(db.DateTime)

    def __init__(self, tag_name, create_time=None):
        self.tag_name = tag_name
        self.create_time = create_time if create_time else datetime.utcnow()

    def __repr__(self):
        return '<Tag %r>' % (self.tag_name)

    def get_id(self):
        return unicode(self.tag_id)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class TagPost(db.Model):
    """
    tag_post model
    """
    __tablename__ = 't_tag_post'

    tag_post_id = Column(db.Integer, primary_key=True)
    post_id = Column(db.Integer)
    tag_id = Column(db.Integer)

    def __init__(self, tag_id, post_id):
        self.tag_id = tag_id
        self.post_id = post_id

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class Pic(db.Model):
    """
    pic model
    """
    __tablename__ = 't_pic'

    pic_id = Column(db.Integer, primary_key=True)
    pic_url = Column(db.String(200))
    is_active = Column(db.Integer)

    def __init__(self, pic_url, is_active=1):
        self.pic_url = pic_url
        self.is_active = is_active

    def __repr__(self):
        return '<Pic %r>' % (self.pic_id)

    def get_id(self):
        return unicode(self.pic_id)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
