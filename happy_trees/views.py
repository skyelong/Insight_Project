#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:18:57 2020

@author: macbook
"""
from flask import render_template, request
from happy_trees import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from happy_trees.a_Model import ModelIt
import urllib

# Python code to connect to Postgres
user = 'macbook' 
host = 'localhost'
dbname = 'birth_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)

@app.route('/')
def image_input():
   return render_template("input.html")

@app.route('/output')
def image_output():
    #get the users image from URL
    img = request.args.get("image_url")
    urllib.request.urlretrieve(img, "/Users/macbook/Box/git_hub/Insight_Project/flask/static/image2.jpg")
    #Run the model
    colors = ModelIt()
    #Calculate the length of the color list for flask
    length = len(colors)
    #Calculate the total price of all individual colors
    total = colors.Price_15_ml.sum()
    return render_template("output2.html", colors = colors, length=length, img=img, total=total)
