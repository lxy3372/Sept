#!/usr/bin/env python
# -*- coding=utf-8 -*-

from application.model.db import db
from application.model.Post import Post, Tag, TagPost, Pic
from flask import session

__author__ = 'Riky'


class PostService(object):

    @staticmethod
    def addPost(self, post_dict):

        if post_dict['tags'] is not None:
            tag_list = post_dict['tags'].split(',')
            for tag in tag_list:
                Tag.tag_name = tag
                db.session.add(Tag)

        Post.post_title = post_dict['post_title'] if post_dict['post_title'] is not None else ""
        Post.post_content = post_dict['post_content'] if post_dict['post_content'] is not None else ""
        Post.post_seo = post_dict['post_seo'] if post_dict['post_seo'] is not None else ""
        Post.is_active = post_dict['is_active'] if post_dict['is_active'] is not None else 1
        Post.user_id = session.get('users')['id']
