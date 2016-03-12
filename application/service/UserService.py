#!/usr/bin/env python
# -*- coding=utf-8 -*-

from application.model.User import User

__author__ = 'Riky'


class UserService(object):

    @staticmethod
    def login(email, password):
        """
        登陆判断
        :param email: str
        :param password: str
        :return: User
        """
        return User.query.filter(User.email==email).filter(User.password==password).first()

    @staticmethod
    def add_user(nickname=None, email=None, pic=None, password=None):
        return User(nickname=nickname, email=email, pic=pic, password=password)
