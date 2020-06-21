#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 12:51:05 2020

@author: macbook
"""

import pandas as pd
paths_df = pd.read_csv('/home/ubuntu/Insight_Project/data/color_data3.csv')

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

dbname = 'colors'
username = 'ubuntu'
pswd = 'DarwinRulez!1'

engine = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
print('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
print(engine.url)

paths_df.to_sql('color_data3', engine, if_exists='replace')