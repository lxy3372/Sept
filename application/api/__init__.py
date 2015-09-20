#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Riky'

from flask import Blueprint

# 定义蓝图
api = Blueprint('api', __name__)

# 引入路由
from . import dota2_api
