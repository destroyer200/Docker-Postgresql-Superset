# https://www.psycopg.org/docs/usage.html

import pandas as pd
import numpy as np

import yfinance as yf
import datetime

def finance(name_finance):
    msft = yf.Ticker(name_finance)
    hist = msft.history(period='max')
    hist['finance'] = name_finance
    hist.reset_index(inplace =True)
    hist['Year'] = hist['Date'].apply(lambda x: x.year)
    hist['Month'] = hist['Date'].apply(lambda x: x.month)
    hist['WeekNum'] = hist['Date'].apply(lambda x: x.isocalendar()[1])
    hist['Day'] = hist['Date'].apply(lambda x: datetime.datetime.strptime(str(x).split(' ')[0], '%Y-%m-%d'))
    return hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends',
                 'Stock Splits', 'finance', 'Year', 'Month', 'WeekNum','Day']]

from os import lstat
lst_finance = ['NKE', 'BB', 'FDX', 'CCL', 'BB.TO', 'LASE', 'URNM',
               'VERO', 'TSLA', 'FTNT', 'CEI', 'OP', 'ADCT']
df = pd.DataFrame({})
for i in lst_finance:
    df = df.append(finance(i))


import psycopg2

# Connect to existing database
conn = psycopg2.connect(
    database="finance",
    user="postgres",
    password="postgres",
    host="host.docker.internal",
    port="2001"
)

# Open cursor to perform database operation
cur = conn.cursor()

if cur is not None:
    print('có database nè ')
else:
    print('no')
#
# #create table
cur.execute("create table finance (dtime timestamp, open_price float, \
            high_price float, low_price float, close_price float, \
            volume integer, dividends float, stock_splits float, \
            finance varchar(20), year integer, month integer, \
            week_num integer, day timestamp);")

#insert data
for i in df.values:
    print(i)
    cur.execute("INSERT INTO finance (dtime , open_price, high_price, low_price, close_price, volume, dividends, \
    stock_splits, finance, year, month, week_num, day) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", i)
conn.commit()

# Query the database
cur.execute("SELECT * FROM finance")
rows = cur.fetchall()
for row in rows:
    print(row)
cur.close()
conn.close()
