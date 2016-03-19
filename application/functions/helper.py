#!/usr/bin/env python
# -*- coding=utf-8 -*-

from functools import wraps
from flask import redirect, session, current_app, flash, url_for, request, render_template

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

        #main
        'index': u"首页",
    }
    title = func_title_dict[func_name]
    return title if title else u"标题"


from math import ceil


class Pagination(object):
    """
    分页模型
    """

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page if per_page > 1 else 1
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
            if num <= left_edge or (num > self.page - left_current - 1 and num < self.page + right_current) or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
