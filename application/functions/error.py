#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Riky'


class ErrorCode(object):
    """
    错误码定义
    """

    #:error = [errcode, errmsg]
    add_error = [1, u'添加失败']
    update_error = [2, u'更新失败']
    login_user_pwd_error = [3, u'登陆账户名或者密码错误']
    login_user_forzen_error = [4, u'账户已被冻结']
    upload_not_found = [5, u'您没有上传任何文件']
    param_error = [6, u'参数错误']
    confirm_pwd_error = [7, u'确认密码与新密码不一致']

    @staticmethod
    def get_err_dict(code, errmsg=None, errcode=None):
        """
        获取错误字典
        :param code: Error.var
        :param errmsg: 强制覆盖msg
        :param errcode: 强制覆盖code
        :return: dict
        """
        err = {
            'ret': False,
            'errcode': code[0] if errcode is None else errcode,
            'errmsg': code[1] if errmsg is None else errmsg
        }
        return err


def make_ret(msg, data=None, code=0):
    """
    自定义正常响应
    :param msg:
    :param data:
    :param code:
    :return: dict
    """
    return {
        'ret': True,
        'errmsg': msg,
        'errcode': code,
        'data': data if data else None
    }
