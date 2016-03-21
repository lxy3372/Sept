#!/usr/bin/env python
# -*- coding=utf-8 -*-


from flask import Flask, request, url_for
from flask_bootstrap import Bootstrap
from main import main as main_blueprint
from admin import admin as admin_blueprint
from config import config
from application.model.db import db
from flask.ext.markdown import Markdown

__author__ = 'Riky'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    db.init_app(app)
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page

    Bootstrap(app)
    Markdown(app)

    return app


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
