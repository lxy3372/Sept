#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import logging


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SESSION_KEY = 'users'
    PAGE_LIMIT = 10
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)%s'
    LOGGING_LOCATION = './flask.log'
    LOGGING_LEVEL = logging.INFO

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