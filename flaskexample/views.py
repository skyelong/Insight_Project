#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:18:57 2020

@author: macbook
"""
from flask import render_template, request
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from flaskexample.a_Model import ModelIt
import urllib

# Python code to connect to Postgres
# You may need to modify this based on your OS, 
# as detailed in the postgres dev setup materials.
user = 'macbook' #add your Postgres username here      
host = 'localhost'
dbname = 'birth_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)

@app.route('/')
@app.route('/index')
def index():
   return render_template("index.html",
      title = 'Home', user = { 'nickname': 'Miguel' },
      )

@app.route('/db2')
def birth_page():
   sql_query = """                                                                       
               SELECT * FROM birth_data_table WHERE delivery_method='Cesarean';          
               """
   query_results = pd.read_sql_query(sql_query,con)
   births = ""
   for i in range(0,10):
       births += query_results.iloc[i]['birth_month']
       births += "<br>"
   return births

@app.route('/db_fancy')
def cesareans_page_fancy():
   sql_query = """
              SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
               """
   query_results=pd.read_sql_query(sql_query,con)
   births = []
   for i in range(0,query_results.shape[0]):
       births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
   return render_template('cesareans.html',births=births)

@app.route('/input')
def image_input():
   return render_template("input.html")

@app.route('/output')
def image_output():
    #pull 'birth_month' from input field and store it
    img = request.args.get("image_url")
    urllib.request.urlretrieve(img, "/Users/macbook/Box/git_hub/flask3/flaskexample/static/image2.jpg")
    #just select the Cesareans  from the birth dtabase for the month that the user inputs
    colors = ModelIt()
    length = len(colors)
    total = colors.Price_15_ml.sum()
    return render_template("output2.html", colors = colors, length=length, img=img, total=total)