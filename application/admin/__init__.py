#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Riky'

from flask import Blueprint

# 定义蓝图
admin = Blueprint('admin', __name__)

# 引入路由
from . import views
