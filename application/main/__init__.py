#!/usr/bin/env python
# -*- coding=utf-8 -*-


from flask import Blueprint

__author__ = 'Riky'

# 定义蓝图
main = Blueprint('main', __name__)

# 引入路由
from . import views

