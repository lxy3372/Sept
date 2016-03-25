#!/usr/bin/env python
# -*- coding=utf-8 -*-

from application.model.db import db
from application.model.Post import Post, Tag, TagPost, Pic
from application.model.User import User
from flask import session
from application.functions.helper import list_remove_repeat, InvalidUsage
from application.functions.error import ErrorCode
from sqlalchemy import func

__author__ = 'Riky'


class PostService(object):
    @staticmethod
    def add_post(post_dict):
        """
        添加文章
        :param post_dict: {post_title,post_content,post_seo,pic_list,is_active,tags,pic_list[]}
        :return: post model
        """

        if post_dict['tags'] is not None:
            tag_list = post_dict['tags'].split(',')
            tag_lists = list_remove_repeat(tag_list)
            tag_str = ""
            tag_list = []
            for tag in tag_lists:
                if tag is not None and len(tag) > 0:
                    tag_obj = Tag.query.filter(Tag.tag_name == tag.lower()).first()
                    if tag_obj is None:
                        tag_obj = Tag(tag_name=tag)
                        db.session.add(tag_obj)
                        db.session.flush()
                    if tag_obj:
                        tag_str += str(tag_obj.tag_id) + ','
                        tag_list.append(tag_obj.tag_id)

            pic_id_str = ""
            if len(post_dict['pic_list']) > 0:
                for pic_str in post_dict['pic_list']:
                    pic_obj = Pic.query.filter(Pic.pic_url == pic_str).first()
                    if pic_obj is None:
                        pic_obj = Pic(pic_str)
                        db.session.add(pic_obj)
                        db.session.flush()
                    if pic_obj:
                        pic_id_str += str(pic_obj.pic_id) + ','

        post_title = post_dict['post_title'] if post_dict['post_title'] is not None else ""
        post_content = post_dict['post_content'] if post_dict['post_content'] is not None else ""
        post_seo = post_dict['post_seo'] if post_dict['post_seo'] is not None else ""
        is_active = post_dict['is_active'] if post_dict['is_active'] is not None else 1
        user_id = session.get('users')['id']
        post_tag_id_str = tag_str.strip(',')
        post_pic_id_str = pic_id_str.strip(',')
        post_type = post_dict['post_type']
        post = Post(title=post_title, content=post_content, seo=post_seo, is_active=is_active, user_id=user_id,
                    post_tag_id_str=post_tag_id_str, post_pic_id_str=post_pic_id_str, type=post_type)

        db.session.add(post)
        db.session.flush()

        if len(tag_list) > 0:
            for tag_id in tag_list:
                tag_post = TagPost(tag_id=tag_id, post_id=post.post_id)
                db.session.add(tag_post)

        return post

    @staticmethod
    def update_posts(post_dict):
        """
        修改文章
        :param post_dict: {post_id,post_title,post_content,post_seo,pic_list,is_active,tags,pic_list[]}
        :return: post model
        """

        if post_dict['tags'] is not None:
            tag_list = post_dict['tags'].split(',')
            tag_lists = list_remove_repeat(tag_list)
            tag_str = ""
            tag_list = []
            for tag in tag_lists:
                if tag is not None and len(tag) > 0:
                    tag_obj = Tag.query.filter(Tag.tag_name == tag.lower()).first()
                    if tag_obj is None:
                        tag_obj = Tag(tag_name=tag)
                        db.session.add(tag_obj)
                        db.session.flush()
                    if tag_obj:
                        tag_str += str(tag_obj.tag_id) + ','
                        tag_list.append(tag_obj.tag_id)

            pic_id_str = ""
            if len(post_dict['pic_list']) > 0:
                for pic_str in post_dict['pic_list']:
                    if len(pic_str) == 0:
                        continue
                    pic_obj = Pic.query.filter(Pic.pic_url == pic_str).first()
                    if pic_obj is None:
                        pic_obj = Pic(pic_str)
                        db.session.add(pic_obj)
                        db.session.flush()
                    if pic_obj:
                        pic_id_str += str(pic_obj.pic_id) + ','

        post = Post.query.get(post_dict['post_id'])
        if post is None:
            raise InvalidUsage(payload=ErrorCode.get_err_dict(ErrorCode.post_not_found))

        post_old_tag_id_str = post.post_tag_id_str

        update = {}
        update[Post.post_title] = post_dict['post_title'] if post_dict['post_title'] is not None else ""
        update[Post.post_content] = post_dict['post_content'] if post_dict['post_content'] is not None else ""
        update[Post.post_seo] = post_dict['post_seo'] if post_dict['post_seo'] is not None else ""
        update[Post.is_active] = post_dict['is_active'] if post_dict['is_active'] is not None else 1
        update[Post.user_id] = session.get('users')['id']
        update[Post.post_tag_id_str] = tag_str.strip(',')
        update[Post.post_pic_id_str] = pic_id_str.strip(',')
        update[Post.post_type] = post_dict['post_type']
        Post.query.filter(Post.post_id == post.post_id).update(update)
        db.session.commit()
        return update

    @staticmethod
    def get_posts_list(limit, page, post_type=None, user_id=None, is_active=None, title=None):
        """
        分页查询
        :param limit:
        :param page:
        :param post_type: 查找类型
        :param user_id: 用户id
        :return:  list[User]
        """
        offset = limit * (page - 1)
        query = db.session.query(Post, User).filter(Post.user_id == User.id);
        if post_type is not None:
            query = query.filter(Post.post_type == post_type)
        if user_id is not None:
            query = query.filter(Post.user_id == user_id)
        if is_active is not None:
            query = query.filter(Post.is_active == is_active)
        if title is not None:
            query = query.filter(Post.post_title.like("%%%s%%" % title))
        posts_list = query.order_by(Post.post_id).limit(limit).offset(offset).all()
        total = query.count()
        return posts_list, total

    @staticmethod
    def get_post_by_id(id):
        """
        获取文章详情
        :param id:
        :return:
        """
        sub = db.session.query(User.nickname, User.id).subquery()
        posts = db.session.query(Post, sub.c.nickname).outerjoin((sub, Post.user_id == sub.c.id)).filter(
            Post.post_id == id).first()
        if posts is None:
            return None
        post_dict = {}
        post_dict['posts'] = posts[0]
        post_dict['nickname'] = posts[1]
        post_dict['tag_obj_list'] = PostService.get_tags_in_id(map(int, post_dict['posts'].post_tag_id_str.split(',')))
        post_dict['pic_obj_list'] = PostService.get_pic_in_id(map(int, post_dict['posts'].post_pic_id_str.split(',')))
        return post_dict

    @staticmethod
    def get_tags_in_id(id_list):
        if id_list is None:
            return None
        return Tag.query.filter(Tag.tag_id.in_(id_list)).all()

    @staticmethod
    def get_pic_in_id(id_list):
        if id_list is None:
            return None
        return Pic.query.filter(Pic.pic_id.in_(id_list)).all()

    @staticmethod
    def get_tags_list(limit, page):
        offset = limit * (page - 1)
        sub = db.session.query(TagPost.tag_id, func.count('1').label('total')).group_by(TagPost.tag_id).subquery()
        tags_list = db.session.query(Tag, sub.c.total).outerjoin((sub, Tag.tag_id == sub.c.tag_id)).order_by(
            Tag.tag_id).limit(limit).offset(offset).all()
        total = Tag.query.count()
        return tags_list, total
