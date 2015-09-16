#!/usr/bin/env python
#-*- coding=utf-8 -*-

__author__ = 'Ricky'

from . import main

@main.route('/')
def main():
    return "hello world"