#!/usr/bin/env python
# -*- coding=utf-8 -*-


from application.functions.helper import get_title_by_func, login_required, templated, Pagination, allowed_file
from application.service.UserService import UserService
from application.service.PostService import PostService
from application.model.User import User
from application.functions.helper import InvalidUsage, InvalidUsagePage
from application.functions.error import make_ret, ErrorCode
from . import admin
from flask import jsonify, request, current_app, render_template, make_response
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import os
from werkzeug.utils import secure_filename

__author__ = 'Riky'


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
    limit = current_app.config['PAGE_LIMIT']
    title = get_title_by_func(get_users.func_name)
    list_obj, total = UserService.get_user_list(limit, page)
    page = Pagination(page, limit, total)
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
            raise InvalidUsage(ErrorCode.get_err_dict(ErrorCode.confirm_pwd_error))
    user_dict = {}
    user_id = request.form['id']
    user_dict[User.email] = request.form['email']
    user_dict[User.nickname] = request.form['nickname']
    user_dict[User.pic] = request.form['pic']
    if request.form['new_password']:
        user_dict[User.password] = request.form['new_password']
    try:
        ret = UserService.update_user_info_by_id(user_id, user_dict)
    except Exception as e:
        raise InvalidUsage(payload=ErrorCode.get_err_dict(ErrorCode.update_error), exception=e)
    return jsonify(make_ret(u'修改成功'))


@admin.route("/admin/do_upload", methods=['POST'])
@login_required
def do_upload():
    files = request.files['file']
    if files and allowed_file(files.filename):
        qiniu_server = Auth(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_SECRET_KEY'])
        bucket_name = current_app.config['QINIU_BUCKET']
        key = secure_filename(files.filename)
        token = qiniu_server.upload_token(bucket_name, key, 3600)
        path = current_app.config['TMP_UPLOAD_DIR']
        localfile = os.path.join(path, key)
        files.save(localfile)
        ret, info = put_file(token, key, localfile)
        if info.status_code == 200:
            src = current_app.config['CDN_DOMAIN'] + '/' + ret['key']
            return jsonify(make_ret(msg=u'上传成功', data=src))
        else:
            raise InvalidUsage(payload=ErrorCode.get_err_dict(code=None, errcode=-1, errmsg=info.error))
    else:
        raise InvalidUsage(payload=ErrorCode.get_err_dict(ErrorCode.upload_not_found))


@admin.route("/admin/posts", methods=['GET'], defaults={'page': 1})
@admin.route("/admin/posts/page/<int:page>", methods=['GET'])
@login_required
@templated(template='admin/posts_list.html')
def get_posts(page):
    limit = current_app.config['PAGE_LIMIT']
    title = get_title_by_func(get_posts.func_name)
    try:
        list_obj, total = UserService.get_user_list(limit, page)
    except Exception as e:
        raise InvalidUsagePage(message=e.message, exception=e)

    page = Pagination(page, limit, total)
    return dict(title=title, list=list_obj, Page=page)


@admin.route("/admin/posts/add", methods=['GET'])
@login_required
@templated(template='admin/posts_add.html')
def add_posts():
    title = get_title_by_func(add_posts.func_name)
    return dict(title=title)


@admin.route("/admin/posts/id/<int:id>", methods=['GET'])
@login_required
@templated(template='admin/posts_update.html')
def update_posts(id):
    title = get_title_by_func(get_users.func_name)
    user = UserService.get_user_by_id(id)
    return dict(title=title, user=user)


@admin.route("/admin/posts/add", methods=['POST'])
@login_required
def do_add_posts():
    post_dict = {}
    # article
    if int(request.form['post_type']) == 1 or int(request.form['post_type']) == 2:
        post_dict['post_title'] = request.form.get('post_title', '')
        post_dict['post_content'] = request.form.get('post_content', '')
        post_dict['post_seo'] = request.form.get('post_seo', '')
        post_dict['post_type'] = request.form.get('post_type')
        post_dict['tags'] = request.form.get('tags', '')
        post_dict['pic_list'] = request.form.getlist('pic_str')
        post_dict['is_active'] = int(request.form.get('is_active', 1))
    else:
        raise InvalidUsage(ErrorCode.get_err_dict(ErrorCode.param_error))

    try:
        PostService.addPost(post_dict)
    except Exception as e:
        raise InvalidUsage(payload=ErrorCode.get_err_dict(ErrorCode.add_error))
    return jsonify(make_ret(u'添加成功'))


@admin.errorhandler(InvalidUsagePage)
def handle_invalid_page(err):
    """
    HTML 异常处理句柄
    """
    err_dict = err.to_dict()
    return render_template('admin/400.html', err_info=err_dict), 400


@admin.errorhandler(InvalidUsage)
def handle_invalid_api(error):
    """
    API 异常处理句柄
    """
    response = jsonify(error.to_dict())
    res = make_response(response)
    return res
