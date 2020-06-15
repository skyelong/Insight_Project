#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 20:00:54 2020

@author: macbook
"""

import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

import pandas as pd


with open(os.path.join(os.path.dirname(__file__),"sql.txt")) as fid:
    cred = [x.strip() for x in fid.readlines()]

dbname = 'colors'
username = cred[0]
pswd = cred[1]


## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
con = None
con = psycopg2.connect(database = dbname, user = "macbook", host='localhost', password=pswd)
print(engine.url)


def df_from_query(query):
    """
    Takes a SQL query and outputs the information to a pandas ddf

    Parameters
    ----------
    query : SQL query
        sql query in postgres format.

    Returns
    -------
    dataframe
        returns a pandas dataframe.

    """
    print(engine.url)
    return pd.read_sql_query(query, con)