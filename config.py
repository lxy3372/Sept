#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASKY_MAIL_SENDER = 'Flasky Admin <me@rikyliu.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'dev': DevelopmentConfig,#开发
    'test': TestingConfig,#测试
    'idc': ProductionConfig,#发布
    'default': DevelopmentConfig #默认
}