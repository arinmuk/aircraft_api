from flask import Flask,render_template
from flask import jsonify,request
import json
from flask_cors import CORS, cross_origin
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
app.config['JSON_SORT_KEYS'] = False
CORS(app, support_credentials=True)

def mongo_coll_read():
     #cursor = colmodels.find()
     modelsdf = pd.DataFrame(list(colmodels.find().sort([('ID', 1)])))
     modelsdf.fillna('')
     modelsdf['DIMAID'].fillna('',inplace=True)
     modelsdf['REGISTRATION'].fillna('',inplace=True)
     modelsdf['SHIPPING'].fillna(0,inplace=True)
     modelsdf['PRICE'].fillna(0,inplace=True)
     modelsdf['PictureID'].fillna('',inplace=True)
     modelsolddf = pd.DataFrame(list(colmodels3.find()))
     solddetailsdf = pd.DataFrame(list(colmodels4.find()))
    #modelsdf = pd.DataFrame(list(colmodels.find()))
     return modelsdf,modelsolddf,solddetailsdf
     #print(cursor)
     #return 'Home21 -read'

fulldf,soldf,solddetailsdf = mongo_coll_read()


@app.route("/")
@cross_origin(supports_credentials=True)
def home():
    return render_template('home.html')

@app.route("/readAircraft")
@cross_origin(supports_credentials=True)
def read():
    res = fulldf
    #del res['_id']
    
    res_fix = res[["ID", "MODEL_NO","DIMAID","WID","AIRLINE", "AIRCRAFT_TYPE","REGISTRATION",  "DESCRIPTION",  "SIZE", "PRICE",  "SHIPPING", "TAX",  "COMPANY", "DATEOFORDER",  "ORDEREDFROM", "PictureID",  "HangarClub"]]
    #res_fix=res_fix.sort_values("ID",inplace=True)
    
    #response.headers.add("Access-Control-Allow-Origin", "*")

    return  jsonify(res_fix.to_dict('records'))


@app.route("/summarizecnt")
@cross_origin(supports_credentials=True)
def sum_model_cnt():
        aircraftdf,res1,res2=mongo_coll_read()
        
        
        air_grp = aircraftdf.groupby(['AIRLINE']).ID.count()
        airgrp=aircraftdf.groupby(['AIRLINE'],as_index=False).agg({"ID":"count"}).rename(columns={'ID':'Count'})
        airgrp=airgrp.sort_values(['Count'],ascending=False)
        top10airgrp=airgrp.head(30)
        return jsonify(top10airgrp.to_dict('records'))
    


@app.route("/airlineDash")
def dashgraphs():

    
    
    
    return render_template ('airlinedashboard.html')


@app.route("/about")
def about():
    return render_template ('about.html')

@app.route("/readSales")
@cross_origin(supports_credentials=True)
def read_summarize():
    res2= solddetailsdf.drop(['ID','AircraftID','Buyer','SaleDate'],axis=1)
    solddf_grp1=res2.groupby(['year','month'],\
        as_index=False).agg({'Listing price':"sum",'Net Recd':"sum",
                            'ListingFee':"sum",
                            'EbayFee':"sum",
                            'PaypalFee':"sum",
                            'Shipping':"sum",
                            'Insurance':"sum",
                            'NetRecd':"sum",
                            'price':"sum",
                            'shipping':"sum",
                            'tax':"sum",
                            'profit_loss':"sum"},
                            )
    
    return jsonify(solddf_grp1.to_dict('records'))
@app.route("/salesgraphs")
def salesgraphs():
    return render_template ('salesplot.html')

@app.route("/searchModels")
def searchModels():
    return render_template('MsearchModels.html')
  


if __name__=='__main__':
    app.run(debug=True)