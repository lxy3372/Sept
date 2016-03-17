#!/usr/bin/env python
# -*- coding=utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'Riky'

engine = create_engine("mysql://root:xiaoyi@localhost:3306/flask", encoding='utf-8', echo=True)
DBSession = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
BaseModel = declarative_base()
