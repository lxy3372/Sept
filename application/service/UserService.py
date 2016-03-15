#!/usr/bin/env python
# -*- coding=utf-8 -*-

from application.model.User import User
from flask import current_app
from flask import session

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
        ret = User.query.filter(User.email == email).filter(User.password == password).first()
        print ret
        if ret is None:
            return False, u'账号或者密码错误', None
        else:
            UserService.start_session(ret)
            return True, u'登陆成功', ret

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
