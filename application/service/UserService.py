#!/usr/bin/env python
# -*- coding=utf-8 -*-

from application.model.User import User
from application.model.db import db
from application.functions.helper import InvalidUsage
from application.functions.error import ErrorCode
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
        :return: boolean
        """
        user = User.query.filter(User.email == email).first()
        if check_password_hash(user.password,password) is False:
            raise InvalidUsage(payload=ErrorCode.get_err_dict(ErrorCode.login_user_pwd_error))
        elif user.is_active != 1:
            return InvalidUsage(payload=ErrorCode.get_err_dict(ErrorCode.login_user_forzen_error))
        else:
            UserService.start_session(user)
            return True

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
        ret = User.query.filter(User.id == id).update(user_dict)
        db.session.commit()
        return ret
