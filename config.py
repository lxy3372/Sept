#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASKY_MAIL_SENDER = 'Flasky Admin <me@rikyliu.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SESSION_KEY = 'users'
    PAGE_LIMIT = 20
    APP_TITLE = u"逗逼-"
    QINIU_ACCESS_KEY = 'CVvTOpZ9i2__LUR7i_O1v5Sv2bs4gALu5e6HX95Z'
    QINIU_SECRET_KEY = 'hMfJGXm7xqBnZnf6yBIiG8-dGxdFNu24AngixLi7'
    QINIU_BUCKET = 'riky'
    TMP_UPLOAD_DIR = "/Users/CHDXY/Workspace/Python/Sept/application/static/upload"
    CDN_DOMAIN = "http://7xi3xm.com1.z0.glb.clouddn.com"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    @staticmethod
    def init_app(app):
        app.config.from_pyfile('./configs/dev.cfg')

class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'dev': DevelopmentConfig,  # 开发
    'test': TestingConfig,  # 测试
    'idc': ProductionConfig,  #发布
    'default': DevelopmentConfig  #默认
}