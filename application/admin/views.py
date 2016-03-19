#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Riky'

from application.functions.helper import get_title_by_func, login_required, templated, Pagination
from application.service.UserService import UserService
from application.model.User import User
from . import admin
from flask import jsonify, request

limit = 20


@admin.route("/admin/panel")
@login_required
@templated(template='admin/panel.html')
def panel():
    title = get_title_by_func(panel.func_name)
    return dict(title=title)


@admin.route("/admin/user", methods=['GET'], defaults={'page': 1})
@admin.route("/admin/user/page/<int:page>", methods=['GET'])
@login_required
@templated(template='admin/user_list.html')
def get_users(page):
    title = get_title_by_func(get_users.func_name)
    list_obj, total = UserService.get_user_list(limit, page)
    page = Pagination(page, page-1, total)
    return dict(title=title, list=list_obj, Page=page)

@admin.route("/admin/user/id/<int:id>", methods=['GET'])
@login_required
@templated(template='admin/user_update.html')
def update_user(id):
    title = get_title_by_func(get_users.func_name)
    user = UserService.get_user_by_id(id)
    return dict(title=title, user=user)


@admin.route("/admin/do_user", methods=['PUT'])
@login_required
def do_update_user():
    if request.form['new_password'] is not None:
        if request.form['new_password'] != request.form['confirm_password']:
            return jsonify({'ret': False, 'errcode': -1, 'errmsg': u'密码不一致'})
    user_dict = {}
    user_id = request.form['id']
    user_dict[User.email] = request.form['email']
    user_dict[User.nickname] = request.form['nickname']
    user_dict[User.pic] = request.form['pic']
    if request.form['new_password']:
        user_dict[User.password] = request.form['new_password']
    ret = UserService.update_user_info_by_id(user_id, user_dict)
    print ret
    if ret == 1:
        ret_dict = {"ret": True, "errcode":0, "errmsg":"修改成功", "data":None}
    else:
        ret_dict = {"ret": False, "errcode":-1, "errmsg":"修改失败", "data":None}

    return jsonify(ret_dict)
