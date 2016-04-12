#!/usr/bin/env python
# -*-  coding=utf-8 -*-

from application import create_app

__author__ = 'Riky'

application = create_app('dev')

if __name__ == '__main__':
    application.run(host='0.0.0.0')
