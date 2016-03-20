#!/usr/bin/env python
# -*- coding=utf-8 -*-

from application.model.db import db
from sqlalchemy import Column, Integer, String, Text, DateTime

__author__ = 'Riky'


class Post(db.Model):
    """
    POST model
    """

    __tablename__ = 't_post'

    post_id = Column(Integer, primary_key=True)
    post_title = Column(String(100))
    post_content = Column(Text)
    post_type = Column(Integer)
    user_id = Column(Integer)
    post_tag_id_str = Column(String(100))
    post_pic_id_str = Column(String(100))
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    is_active = Column(Integer)
    post_seo = Column(String(255))

    def __init__(self, id, title, content, type, user_id, post_tag_id_str=None, post_pic_id_str=None, is_active=1,
                 seo=None):
        self.post_id = id
        self.post_title = title
        self.post_content = content
        self.post_type = type
        self.user_id = user_id
        self.post_tag_id_str = post_tag_id_str
        self.post_pic_id_str = post_pic_id_str
        self.is_active = is_active
        self.post_seo = seo


class Tag(db.Model):
    """
    tag model
    """
    __tablename__ = 't_tag'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(100))
    create_time = Column(DateTime)

    def __init__(self, tag_id, tag_name):
        self.tag_id = tag_id
        self.tag_name = tag_name


class TagPost(db.Model):
    """
    tag_post model
    """
    __tablename__ = 't_tag_post'

    tag_post_id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    tag_id = Column(Integer)

    def __init__(self, tag_id, post_id):
        self.tag_id = tag_id
        self.post_id = post_id


class Pic(db.Model):
    """
    pic model
    """
    __tablename__ = 't_pic'

    pic_id = Column(Integer, primary_key=True)
    pic_url = Column(String(200))
    is_active = Column(Integer)

    def __init__(self, pic_id, pic_url, is_active):
        self.pic_id = pic_id
        self.pic_url = pic_url
        self.is_active = is_active

