#!/usr/bin/env python
# -*- coding=utf-8 -*-


from flask import Flask, request, url_for, session, render_template
from flask_bootstrap import Bootstrap
from main import main as main_blueprint
from admin import admin as admin_blueprint
from config import config
from application.model.db import db
from datetime import datetime
import logging

__author__ = 'Riky'

app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    db.init_app(app)
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page

    hander = logging.FileHandler(app.config['LOGGING_LOCATION'])
    hander.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    hander.setFormatter(formatter)
    app.logger.addHandler(hander)

    Bootstrap(app)

    return app


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


@app.template_filter('hello')
def reverse_filter(f):
    now = datetime.now()
    date = now.strftime('%p')
    name = session.get(app.config.get('SESSION_KEY'))['nickname']
    return (u"上午好" if date == 'AM' else u"下午好") + u"，" + name


@app.template_filter('is_active')
def is_active(flag):
    return u"发布" if flag == 1 else u"未发布"


@app.template_filter('post_type')
def post_type(type):
    type_dict = {
        '1': u'文章',
        '2': u'图片'
    }
    return type_dict[str(type)]


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    else:
        db.session.commit()
    db.session.remove()


@app.errorhandler(404)
def page_not_found(e):
    app.logger.info('page not found: %s', (request.path))
    return render_template('404.html'), 404
