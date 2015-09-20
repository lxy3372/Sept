#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Riky'

from flask import jsonify
from . import api


@api.route('/api/v1/get_user', methods=['GET'])
def get_user_info():
    ex1 = {
        'title': 'test',
        'content': 'This is dota2 api test1'
    }
    return jsonify(ex1)
