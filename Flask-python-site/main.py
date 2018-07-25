from flask import Flask, render_template
from flask import request
import datetime
from pymongo import MongoClient
import requests
import os
from displayMap import DisplayMaps
app = Flask(__name__)
collectionMap = DisplayMaps()
client = MongoClient('mongodb://localhost:27017/')
db = client.Accidents

@app.route("/")
def index():
    try :
        return render_template('index.html')
    except Exception, e:
        return str(e)

@app.route("/about")
def about():
    try :
        return render_template('dataset.html')
    except Exception, e:
        return str(e)

@app.route("/collections/<collection>/<columnName>")
def getcollection(collection, columnName):
    try :
        initialTimeStamp=datetime.datetime.now()
        collection = str(collection)
        columnName = str(columnName)
        cursor = list(db[collection].find({},{columnName:1, '_id': 0}))
        loadDuration=datetime.datetime.now() - initialTimeStamp
        data = [movie[columnName] for movie in cursor]
        labels = list(set(data))
        ssData = []
        for lbl in labels:
                ssData.append(data.count(lbl))

        collectionName = collectionMap[collection]['displayName']

        if collectionMap.get(columnName) :
            print('col name if')
            columnMap = collectionMap[columnName]
            columnName = collectionMap[columnName]['displayName']            
            legend = columnMap['legend']
        else :
            legend = [{'name' : 'NA',
                        'displayName': 'Not Available'}]
            columnName = '{' + columnName + '}'


            

        ssData=list(ssData)
        chartData={'labels':labels,'ssData': ssData}
        return render_template('collection.html', columnName=columnName, collection=collectionName, chartData=chartData,loadDuration=loadDuration, legends=legend)
    except Exception, e:
        return str(e)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True, port=int(os.getenv('PORT', '5000')))
