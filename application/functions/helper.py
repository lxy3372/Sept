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
        'panel': u"控制面板",
        'login_page': u"登陆",
        'index': u"首页",
    }
    title = func_title_dict[func_name]
    return title if title else u"标题"
