import json
#from flask import Flask,render_template
#from flask import jsonify,request
from flask import jsonify,request
from flask import Flask,render_template
from flask_cors import CORS, cross_origin
from config import cloudM,cloudMpassword,sqluser,sqlpass,servername
from pymongo import MongoClient
from search import DistinctAirline_cloudM_R,SearchAirline_cloudM_R,DistinctRegistration_cloudM_R,SearchRegistration_cloudM_R,cloudM_R
import pandas as pd
import numpy as np
from dash_data import collection_summary,pivotdatasum

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
@app.route("/PivotDash")
def Pivotgraphs():
   #netcount_costdf,netcount_spl_costdf =collection_summary()
    
        
    
   #return jsonify(netcount_spl_costdf.to_dict('records'))
   return render_template ('wbrFusion.html')
@app.route("/PivotDashData")
def Pivotdata():
   #netcount_costdf,netcount_spl_costdf =collection_summary()
    
        pv_df=pivotdatasum()
        #del ressolddetails['_id']
        pv_df.head()
        return jsonify(pv_df.to_dict('records'))



#+++++++++++++++++++++++++++

@app.route("/dash_pane5/<choice>")
def dash_pane5(choice):
    
    cloudmodelsdf,cloudsoldmodelsdf,cloudsolddetails,cloudairlinescalecount,cloudairlinescalecost = cloudM_R()
    panedf,panedf2=collection_summary()
    calcdf = cloudmodelsdf#.drop(['DIMAID', 'WID','DESCRIPTION', 'PICTURE', 'Picture2','Picture3', 'Rare', 'HangarClub', 'MarketValue', 'PictureID'],axis =1)
    airlinetotal=calcdf.groupby(['SIZE'],as_index=False).agg({'PRICE':'sum','ID':'count'}).rename(columns={'ID':"Total_Models"})
    
    
    #distinctAirlinedf.head()
    #data_dict=distinctAirlinedf.to_dict('records')
    #panedf_dict = panedf.to_dict('records')
    #panedf2_dict=panedf2.to_dict('records')
    selection=choice
    tot_summary=pd.DataFrame()
    if selection =="All":
        tot_summary=panedf2.copy()   
    else:
        filterstr = panedf2["Size"]==selection
        tot_summary=panedf2.where(filterstr,inplace=False)
        
    tot_summary=tot_summary.dropna()
    tot_summary=tot_summary.rename(columns={"myCount":"ModelCount"})
    return jsonify(tot_summary.to_dict('records'))



@app.route("/dash_pane1")
def dash_pane1():
    
    cloudmodelsdf,cloudsoldmodelsdf,cloudsolddetails,cloudairlinescalecount,cloudairlinescalecost = cloudM_R()
    panedf,panedf2=collection_summary()
    calcdf = cloudmodelsdf#.drop(['DIMAID', 'WID','DESCRIPTION', 'PICTURE', 'Picture2','Picture3', 'Rare', 'HangarClub', 'MarketValue', 'PictureID'],axis =1)
    airlinetotal=calcdf.groupby(['SIZE'],as_index=False).agg({'PRICE':'sum','ID':'count'}).rename(columns={'ID':"Total_Models"})
    
    
    #distinctAirlinedf.head()
    #data_dict=distinctAirlinedf.to_dict('records')
    panedf_dict = panedf.to_dict('records')
    panedf2_dict=panedf2.to_dict('records')
    return render_template("home.html", data = panedf_dict, alldata=panedf2_dict)

@app.route("/dash_pane2")
def dash_pane2():
    
    
    panedf,panedf2=collection_summary()
    
    #distinctAirlinedf.head()
    #data_dict=distinctAirlinedf.to_dict('records')
    #panedf_dict = panedf.to_dict('records')
    panedf = panedf.rename(columns={"myCount":"ModelCount"})
    panedf_dict=panedf.to_dict('records')
    return jsonify(panedf.to_dict('records'))

@app.route("/dash_pane3/<choice>")
def dash_pane3(choice):
    
    selection=choice
    panedf,panedf2=collection_summary()
    if selection =="All":
        total_summary_all = panedf2.groupby('Size',as_index=False).sum(['total','myCount'])
        
    else:
        filterstr = panedf2["Size"]==selection
        total_summary=panedf2.where(filterstr,inplace=False)
        totalairlines= total_summary['Airline'].nunique()
        print(totalairlines)
        total_summary =total_summary.groupby('Size',as_index=False).sum(['total','myCount'])
        total_summary['airlineCount']=totalairlines
        
        total_summary_all = total_summary
    total_summary_all = total_summary_all.rename(columns={"myCount":"ModelCount"})   
    #distinctAirlinedf.head()
    #data_dict=distinctAirlinedf.to_dict('records')
    panedf_dict = panedf.to_dict('records')
    panedf2_dict=panedf2.to_dict('records')
    return jsonify(total_summary_all.to_dict('records'))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route("/ScaleSize")
def Sizedata():
   #netcount_costdf,netcount_spl_costdf =collection_summary()
        panedf,panedf2=collection_summary()
        #size_dict={}
        
        s=panedf2["Size"].unique()
        s=np.insert(s,0,"All")
        #sizedf=pd.DataFrame(panedf2["Size"].unique())
        #sizedf.rename(columns={0:"Size"},inplace=True)
        #size_dict=sizedf.to_json(orient='records')
        #size_dict
        return jsonify(list(s))#size_dict



if __name__=='__main__':
    app.run(debug=True)