#!/usr/bin/env python
# -*- coding=utf-8 -*-


from flask import render_template, flash, redirect, jsonify, request, url_for
from application.service.UserService import UserService
from application.functions.error import make_ret, ErrorCode
from application.functions.helper import login_required, get_title_by_func, templated, InvalidUsagePage, InvalidUsage
from application.service.PostService import PostService
from . import main

__author__ = 'Ricky'


@main.route('/index')
@main.route('/')
@templated(template='index.html')
def index():
    """
    Home page
    """
    title = get_title_by_func(index.func_name)
    page = request.args.get('p')
    page = page if page > 0 else 1
    return render_template('index.html', title=title, page=page)


@main.route('/posts/page/<int:page>', methods=['GET'])
def get_posts_by_page(page):
    """
    ajax 加载分组数据
    """
    page = page if page > 0 else 1
    post_data, total = PostService.get_posts_dicts(limit=5, page=page)
    if post_data is None:
        raise InvalidUsage(ErrorCode.get_err_dict(ErrorCode.post_list_not_found))
    is_end = True if total <= page*5 else False
    return jsonify(make_ret(msg='ok', data={'list': post_data, 'total': total, 'is_end': is_end}))


@main.route('/id/<int:id>', methods=['GET'])
@templated(template='post.html')
def post(id):
    """
    Post detail by post_id
    :param id: post_id
    """
    post_data = PostService.get_post_by_id(id)
    if post_data is None:
        raise InvalidUsagePage(ErrorCode.get_err_dict(ErrorCode.post_not_found), status_code=404)
    title = post_data['posts'].post_title
    return dict(title=title, data=post_data)


@main.route('/post/<string:seo_key>', methods=['GET'])
@templated(template='post.html')
def post_by_key(seo_key):
    """
    Post detail by post_seo
    :param seo_key:  post_seo
    """
    post_data = PostService.get_post_by_seo_key(seo_key)
    if post_data is None:
        raise InvalidUsagePage(ErrorCode.get_err_dict(ErrorCode.post_not_found), status_code=404)
    title = post_data['posts'].post_title
    return dict(title=title, data=post_data)


@main.route('/about')
def templates(anything=None):
    """
    About page
    """
    return "hello world"


@main.route('/login', methods=['GET'])
@templated(template='login.html')
def login_page():
    """
    Login page
    """
    title = get_title_by_func(login_page.func_name)
    return dict(option='', title=title)


@main.route('/do_login', methods=['POST'])
def do_login():
    """
    Ajax login
    :return:
    :rtype:
    """
    email = request.form['email']
    password = request.form['password']
    ret = UserService.login(email, password)
    return jsonify(make_ret(msg=u'登陆成功', data=url_for('admin.panel')))


@main.route("/logout")
@login_required
def logout():
    """
    log out
    """
    UserService.logout()
    flash("Logged out.")
    return redirect('/login')


@main.errorhandler(InvalidUsagePage)
def page_error(err):
    error_dict = err.to_dict()
    return render_template('400.html', error_info=error_dict), 400


@main.errorhandler(InvalidUsage)
def handle_invalid_api(error):
    """
    API 异常处理句柄
    """
    response = jsonify(error.to_dict())
    return response


@main.teardown_app_request
def shutdown_session(exception=None):
    pass
