#!/usr/bin/env python
#-*- coding=utf-8 -*-

__author__ = 'Ricky'


from flask import Blueprint

#定义蓝图
main = Blueprint('main', __name__)

#引入路由
from . import views