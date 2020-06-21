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

@app.route('/')
def image_input():
   return render_template("input.html")

@app.route('/output')
def image_output():
    #get the users image from URL
    img = request.args.get("image_url")
    urllib.request.urlretrieve(img, '/home/ubuntu/Insight_Project/happy_trees/static/image2.jpg')
    #Run the model
    colors = ModelIt()
    #Calculate the length of the color list for flask
    length = len(colors)
    #Calculate the total price of all individual colors
    total = colors.Price_15_ml.sum()
    savings = total - 35.19
    savings = format(savings, '.2f')
    
    return render_template("output.html", colors = colors, length=length, img=img, total=total, savings=savings)

@app.route('/3_color')
def three_color():
   return(render_template("3_color.html")
