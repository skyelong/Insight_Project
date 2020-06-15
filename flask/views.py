#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:18:57 2020

@author: macbook
"""

from flaskexample import app

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"