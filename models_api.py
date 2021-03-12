from flask import Flask,render_template
from flask import jsonify,request
import json
from config import cloudM,cloudMpassword
from pymongo import MongoClient
import pandas as pd
client = MongoClient()
client = MongoClient(("mongodb+srv://"+ cloudM + ":"
                       + cloudMpassword + "@cluster0-omshy.mongodb.net/test?retryWrites=true&w=majority"))
db=client['Aircraft']
colmodels=db['models']
colmodels2=db['models2']
colmodels3=db['modelsold']
colmodels4=db['solddetails']
#cursor = colmodels.find()

app=Flask(__name__)


def mongo_coll_read():
     #cursor = colmodels.find()
     modelsdf = pd.DataFrame(list(colmodels.find().sort([('ID', 1)])))
     modelsolddf = pd.DataFrame(list(colmodels3.find()))
     solddetailsdf = pd.DataFrame(list(colmodels4.find()))
    #modelsdf = pd.DataFrame(list(colmodels.find()))
     return modelsdf,modelsolddf,solddetailsdf
     #print(cursor)
     #return 'Home21 -read'

fulldf,soldf,solddetailsdf = mongo_coll_read()


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/readAircraft")
def read():
    res = fulldf
    #del res['_id']
    
    res_fix = res[["ID", "MODEL_NO","DIMAID","WID","AIRLINE", "AIRCRAFT_TYPE","REGISTRATION",  "DESCRIPTION",  "SIZE", "PRICE",  "SHIPPING", "TAX",  "COMPANY", "DATEOFORDER",  "ORDEREDFROM", "PictureID",  "HangarClub"]]
    #res_fix=res_fix.sort_values("ID",inplace=True)
    return jsonify(res_fix.to_dict('records'))
    return res

@app.route("/about")
def about():
    return render_template ('about.html')
@app.route("/salesgraphs")
def salesgraphs():
    return render_template ('soldgraphs/index1.html')

@app.route("/searchModels")
def searchModels():
    return render_template('index2.html')
  


if __name__=='__main__':
    app.run(debug=True)