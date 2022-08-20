from flask import Flask,render_template
from flask import jsonify,request
import json
from flask_cors import CORS, cross_origin
from config import cloudM,cloudMpassword
from pymongo import MongoClient
from search import DistinctAirline_cloudM_R,SearchAirline_cloudM_R,DistinctRegistration_cloudM_R,SearchRegistration_cloudM_R
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
        bins=[1,50,100,150,200,250,300,400,500]
        group_names = ["<50", "<100", "<150", "<200", "<250","<300","<400","<500"]
        
        top10airgrp["Group_Count"] = pd.cut(top10airgrp["Count"], bins, labels=group_names, include_lowest=True)
        top10airgrp
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
  

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++search code
def readdata():
    alldatadf = fulldf
    #,allsolddetdf,allsoldtrans=cloudM_R()
    return alldatadf


@app.route("/send", methods=["GET", "POST"])
def sendairline():
    
    print(request.method)
    
    if request.method == "POST":
          nickname = request.form["airline"]
          print("apple")
          print(nickname) 
          airecords_df=SearchAirline_cloudM_R(nickname)
      #    res_fix = airecords_df[["ID", "MODEL_NO","DIMAID","WID","AIRLINE", "AIRCRAFT_TYPE","REGISTRATION",  "DESCRIPTION",  "SIZE", "PRICE",  "SHIPPING", "TAX",  "COMPANY", "DATEOFORDER",  "ORDEREDFROM", "PictureID",  "HangarClub"]]
      #  return jsonify(res_fix.to_dict('records'))
          columnslst=airecords_df.columns
          print(columnslst)
          if columnslst[0]=="_id":
                    del airecords_df['_id']
          
          filterdata_dict=airecords_df.to_dict('records')
          UAirdf=DistinctAirline_cloudM_R()
          UAirdf.rename(columns={0:"Airline"},inplace=True)
          data_dict = UAirdf.to_dict('records')
          print(data_dict)
          labelval=nickname
    return render_template("formsearch.html",data = data_dict,alldata=filterdata_dict,airlinename=labelval)

@app.route("/uniqueAirlines")
def retrieveairline():
    
    UAirdf=DistinctAirline_cloudM_R()
    UAirdf.rename(columns={0:"Airline"},inplace=True)
    tempdata=jsonify(UAirdf.to_dict('records'))
    alldatadf=readdata()
    
    columnslst=alldatadf.columns
    print(columnslst)
    if columnslst[0]=="_id":
            del alldatadf['_id']
    
    
    
    #distinctAirlinedf.head()
    #data_dict=distinctAirlinedf.to_dict('records')
    data_dict = UAirdf.to_dict('records')
    alldata_dict=alldatadf.to_dict('records')
    return render_template("formsearch.html", data = data_dict, alldata=alldata_dict)




#++++++++++++++++++++++++++

@app.route("/sendReg", methods=["GET", "POST"])
def sendreg():
    
    print(request.method)
    
    if request.method == "POST":
          nickname = request.form["registration"]
          print("apple")
          print(nickname) 
          airecords_df=SearchRegistration_cloudM_R(nickname)
      #    res_fix = airecords_df[["ID", "MODEL_NO","DIMAID","WID","AIRLINE", "AIRCRAFT_TYPE","REGISTRATION",  "DESCRIPTION",  "SIZE", "PRICE",  "SHIPPING", "TAX",  "COMPANY", "DATEOFORDER",  "ORDEREDFROM", "PictureID",  "HangarClub"]]
      #  return jsonify(res_fix.to_dict('records'))
          columnslst=airecords_df.columns
          print(columnslst)
          if columnslst[0]=="_id":
                    del airecords_df['_id']
          
          filterdata_dict=airecords_df.to_dict('records')
          UAirdf=DistinctRegistration_cloudM_R()
          UAirdf.rename(columns={0:"Registration"},inplace=True)
          data_dict = UAirdf.to_dict('records')
          print(data_dict)
          labelval=nickname
    return render_template("frmsearchreg.html",data = data_dict,alldata=filterdata_dict,airlinename=labelval)

@app.route("/uniqueReg")
def retrieve_reg():
    
    UAirdf=DistinctRegistration_cloudM_R()
    UAirdf.rename(columns={0:"Registration"},inplace=True)
    tempdata=jsonify(UAirdf.to_dict('records'))
    alldatadf=readdata()
    columnslst=alldatadf.columns
    print(columnslst)
    if columnslst[0]=="_id":
            del alldatadf['_id']
    #distinctAirlinedf.head()
    #data_dict=distinctAirlinedf.to_dict('records')
    data_dict = UAirdf.to_dict('records')
    alldata_dict=alldatadf.to_dict('records')
    return render_template("frmsearchreg.html", data = data_dict, alldata=alldata_dict)








#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





if __name__=='__main__':
    app.run(debug=True)