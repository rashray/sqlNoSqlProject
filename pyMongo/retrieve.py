# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 23:16:04 2018

@author: SM
"""
from pymongo import MongoClient
import pandas as pd
import json
import datetime

client = MongoClient('mongodb://localhost:27017/')

db = client.Accidents_demo
print('------------Initial List=', db.collection_names())

collections = ['caracteristics']
# collections = ['caracteristics', 'places', 'users', 'vehicles']

i = 0
while i < len(collections):
    print('********************************************************************************')
    initialTimeStamp=datetime.datetime.now()
    print("LOADING...", collections[i])
    collectionName = collections[i]
    csvName = 'accidents-in-france-from-2005-to-2016/' + str(collections[i]) + '.csv'
    data = pd.read_csv(csvName, encoding = "ISO-8859-1")
    payload = json.loads(data.to_json(orient='records'))
    readTimeStamp=datetime.datetime.now()
    readTime = readTimeStamp - initialTimeStamp
    print('***********DATA READ FOR', collections[i], 'in', readTime)
    collection = db[collectionName]
    collection.insert_many(payload)
    loadTimeStamp=datetime.datetime.now()
    loadTime = loadTimeStamp - readTimeStamp
    print('***********ATA LOADED FOR', collections[i], 'in', loadTime)
    i += 1
client.close()
print('----------Final List', db.collection_names())
print('Process Complete')

