#!/usr/bin/env python
# -*- coding=utf-8 -*-

from functools import wraps
from flask import redirect, session, current_app, flash, url_for, request, render_template
from math import ceil

__author__ = 'Riky'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get(current_app.config.get('SESSION_KEY')):
            flash(u'没有登陆')
            return redirect(url_for('main.login_page'))
        return f(*args, **kwargs)

    return decorated_function


def templated(template=None):
    """
    模板装饰器
    :param template 模板路径
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)

        return decorated_function

    return decorator


def get_title_by_func(func_name):
    """
    返回页面标题
    :param func_name: 方法名
    :return: unicode str
    """
    func_title_dict = {
        # admin
        'panel': u"控制面板",
        'login_page': u"登陆",
        'get_users': u"用户管理",
        'update_user': u"用户管理",
        'get_posts': u"文章管理",
        'add_posts': u"文章管理",
        'get_tags': u"文章管理",

        # main
        'index': u"首页",
    }
    title = func_title_dict[func_name]
    return title if title else u"标题"


class Pagination(object):
    """
    分页模型
    """

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or (
                            num > self.page - left_current - 1 and num < self.page + right_current) or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def allowed_file(filename):
    """
    允许上传的文件后缀
    :param filename:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ['png', 'jpg', 'jpeg', 'gif']


def list_remove_repeat(list):
    """
    list去重复
    """
    new_list = []
    for id in list:
        if id not in new_list:
            new_list.append(id)
    return new_list


class InvalidUsage(Exception):
    """
    RESTFul API 反馈错误
    """
    status_code = 400

    def __init__(self, status_code=None, payload=None, exception=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        if exception is not None and isinstance(exception, Exception):
            #TODO log
            pass

    def to_dict(self):
        rv = dict(self.payload or ())
        return rv


class InvalidUsagePage(Exception):
    status_code = 400

    def __init__(self, message=None, status_code=None, payload=None, data=None, exception=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.data = data
        self.message = message if message is not None else ""
        if exception is not None and isinstance(exception, Exception):
            #TODO log
            pass

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['data'] = self.data
        rv['message'] = self.message
        return rv
