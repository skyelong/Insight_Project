#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:43:37 2020

@author: macbook
"""
from joblib import dump, load
import numpy as np
import cv2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import matplotlib.pyplot as plt

#set the directory for custom scripts
import sys
sys.path.append('/Users/macbook/Box/git_hub/Insight_Project_clean/scripts/')

#import custom scripts
import sql_con
from sql_con import df_from_query
import hsv_shift as hsv


def ModelIt(fromUser  = 'Default'):
    hsv_knn_chroma = load('/Users/macbook/Box/git_hub/Insight_Project_clean/models/ds_h_chroma.joblib')
    hsv_knn_neutral = load('/Users/macbook/Box/git_hub/Insight_Project_clean/models/ds_h_neutrals.joblib')
    pixels = hsv.import_convert_pixelize("/Users/macbook/Box/git_hub/flask3/flaskexample/static/image2.jpg")
    
    shifted_colors, shifted_neutrals = hsv.shift_h_split(pixels, .25, .25)
    
    #cluster using K-means
    X_pixels = shifted_colors[['h']]

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=8, random_state=42, algorithm = 'full')
    kmeans.fit(X_pixels)
    image2show = kmeans.cluster_centers_[kmeans.labels_]
    
    kmeans_df = pd.DataFrame(image2show, columns=['h'])
    kmeans_df['label'] = kmeans.labels_
    
    X = kmeans_df[['h']]
    
    #cluster the colors

    predict_colors = hsv_knn_chroma.predict(X)
    
    colors2 = np.array(np.unique(predict_colors, return_counts=True)).T
    
    colors2df = pd.DataFrame(colors2, columns = ['name', 'count'])
    
    names = colors2df[colors2df['count']>1000].sort_values(by=['count'], ascending = False)
    
    names
    print(names)
    
    #scluser the neutrals
    X_pixels_n = shifted_neutrals[['h']]

    from sklearn.cluster import KMeans
    kmeans_n = KMeans(n_clusters=2, random_state=42, algorithm = 'full')
    kmeans_n.fit(X_pixels_n)
    image2show_n = kmeans_n.cluster_centers_[kmeans_n.labels_]
    
    kmeans_df_n = pd.DataFrame(image2show_n, columns=['h'])
    kmeans_df_n['label'] = kmeans_n.labels_
    
    kmeans_df_n
    
    X_n = kmeans_df_n[['h']]
    predict_neutrals = hsv_knn_neutral.predict(X_n)
    neutrals = np.array(np.unique(predict_neutrals, return_counts=True)).T
    neutrals_df = pd.DataFrame(neutrals, columns = ['name', 'count'])
    names_n = neutrals_df.sort_values(by=['count'], ascending = False)
    names_n
    
    #get SQL
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    dbname = 'colors'
    username = 'macbook'
    pswd = 'DarwinRulez!1'
    
    engine = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
    print('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
    print(engine.url)
    
    con = None
    con = psycopg2.connect(database = dbname, user = username, host='localhost', password=pswd)
    
    def sql_query_from_list(list):
        test = pd.DataFrame()
        list_param = []
        for i in range(0,len(list)):
            color = list[i]
            sql_param = """SELECT * FROM web_data
            WHERE name = %(color)s"""
            param = pd.read_sql_query(sql_param,con, params = {'color':color})
            test = pd.concat([test,param], axis = 0, ignore_index=True)
        return test 
    
    neutral_names = names_n.name.value_counts().index.to_list()
    color_names = names.name.value_counts().index.to_list()
    colors = sql_query_from_list(color_names)
    neutrals = sql_query_from_list(color_names)
    return colors