#!/usr/bin/env python
# -*- coding=utf-8 -*-

from application.model.User import User
from flask import current_app, session
from werkzeug.security import generate_password_hash, check_password_hash

__author__ = 'Riky'


class UserService(object):
    @staticmethod
    def login(email, password):
        """
        登陆判断
        :param email: str
        :param password: str
        :return: (errcode, errmsg, data)
        """
        user = User.query.filter(User.email == email).first()
        if check_password_hash(user.password,password) is False:
            return False, u'账号或者密码错误', None
        else:
            UserService.start_session(user)
            return True, u'登陆成功', user

    @staticmethod
    def add_user(nickname=None, email=None, pic=None, password=None):
        return User(nickname=nickname, email=email, pic=pic, password=password)

    @staticmethod
    def start_session(user):
        """
        :param user
        :return bool
        """
        # session format
        user_json = {'id': user.id, 'nickname': user.nickname, 'email': user.email, 'pic': user.pic}
        session[current_app.config.get('SESSION_KEY')] = user_json
        return True

    @staticmethod
    def logout():
        """
        :return: bool
        """
        if session.pop(current_app.config.get('SESSION_KEY'), None):
            return True
        else:
            return False

    @staticmethod
    def get_user_list(limit, page):
        offset = limit * (page - 1)
        list = User.query.limit(limit).offset(offset).all()
        total = User.query.count()
        return list, total

    @staticmethod
    def get_user_by_id(id):
        user = User.query.filter(User.id == id).first()
        return user

    @staticmethod
    def update_user_info_by_id(id, user_dict):
        """
        更新用户资料
        :param id: userid
        :param user_dict: {User.id:1, ...}
        :return: int
        """
        if user_dict.has_key(User.password):
            user_dict[User.password] = generate_password_hash(user_dict[User.password])
        return User.query.filter(User.id == id).update(user_dict)
