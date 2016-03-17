#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'Riky'

from application.functions.helper import get_title_by_func, login_required, templated
from . import admin

@admin.route("/admin/panel")
@login_required
@templated(template='admin/panel.html')
def panel():
    title = get_title_by_func(panel.func_name)
    return dict(option='', title=title)
