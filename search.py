import sys
import pandas as pd
#import pyodbc as pyodbc
from sqlalchemy.dialects.mssql import pymssql
from sqlalchemy import create_engine, MetaData, Table, select
import sqlalchemy
#import pymssql
import pymongo
import csv
import json
from config import cloudM,cloudMpassword,sqluser,sqlpass
from pymongo import MongoClient
from flask import Flask, jsonify, render_template
#from elasticsearch import Elasticsearch

#local mongo install
#client = MongoClient()
#client = MongoClient('localhost', 27017)

#cloud mongo connect
cloudMClnt=MongoClient()
cloudMClnt=MongoClient("mongodb+srv://"+ cloudM + ":"+ cloudMpassword + "@cluster0-omshy.mongodb.net/test?retryWrites=true&w=majority")


#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#es

#from sqlalchemy import create_engine, MetaData, Table, select
#connection = pymssql.connect(host='Zbook',user=sqluser, password=sqlpass,database='Aircraft')

# read cloud Mongo Data and return dataframes


def SearchAirline_cloudM_R(airlinename):
    db=cloudMClnt['Aircraft']
    colmodels=db['models']
    airline=airlinename
    
    
    modelsdf = pd.DataFrame(list(colmodels.find({'AIRLINE':airline}).sort([('ID', 1)])))
    
    return modelsdf
def SearchRegistration_cloudM_R(registration):
    db=cloudMClnt['Aircraft']
    colmodels=db['models']
    reg=registration
    
    
    modelsdf = pd.DataFrame(list(colmodels.find({'REGISTRATION':reg}).sort([('ID', 1)])))
    
    return modelsdf

def DistinctAirline_cloudM_R():
    db=cloudMClnt['Aircraft']
    colmodels=db['models']
    
    
    distinctmodelsdf = pd.DataFrame(list(colmodels.distinct('AIRLINE')))
    
    return distinctmodelsdf

def DistinctRegistration_cloudM_R():
    db=cloudMClnt['Aircraft']
    colmodels=db['models']
    
    
    distinctmodelsdf = pd.DataFrame(list(colmodels.distinct('REGISTRATION')))
    
    return distinctmodelsdf

def cloudM_R():
    db=cloudMClnt['Aircraft']
    colmodels=db['models']
    colmodels2=db['models2']
    colmodels3=db['modelsold']
    colmodels4=db['solddetails']
    colair_sc_cnt=db['air_scale_cnt']
    colair_sc_cost=db['air_scale_cost']
    modelsdf = pd.DataFrame(list(colmodels.find().sort([('ID', 1)])))
    modelsolddf = pd.DataFrame(list(colmodels3.find()))
    solddetailsdf = pd.DataFrame(list(colmodels4.find()))
    colair_sc_cntdf = pd.DataFrame(list(colair_sc_cnt.find()))
    colair_sc_costdf = pd.DataFrame(list(colair_sc_cost.find()))
    
    #modelsdf = pd.DataFrame(list(colmodels.find()))
    return modelsdf,modelsolddf,solddetailsdf,colair_sc_cntdf,colair_sc_costdf

def createdummy(modelscoldf1):
    cnt=0
    mth=1
    lstdump=[]

    temprecdf = pd.DataFrame()#columns = ["ID","AIRLINE", "month", "year"])
    uair=modelscoldf1['AIRLINE'].unique()
    uair
    for airline in uair:
        for j in range (2000,2024):
            dumpdict={}
            dumpdict['ID']=cnt
            dumpdict['AIRLINE']=airline
            dumpdict['month']=mth
            dumpdict['year']=j
            lstdump.append(dumpdict)
        
        





   
    temprecdf = pd.DataFrame(lstdump)
    return temprecdf


def dataanimation():
    #db=cloudMClnt['Aircraft']
    #colmodelscloud=db['models']
    #modelscoldf = pd.DataFrame(list(colmodelscloud.find().sort([('ID', 1)])))
    #modelscoldf["month"]=modelscoldf["DATEOFORDER"].dt.month
    #modelscoldf["year"]=modelscoldf["DATEOFORDER"].dt.year
    #modelscoldf= modelscoldf.drop(['_id','MODEL_NO','DIMAID','WID','AIRCRAFT_TYPE','REGISTRATION','DESCRIPTION','SIZE','PRICE','SHIPPING','TAX','COMPANY','ORDEREDFROM','DATEOFORDER','PictureID','HangarClub'],axis=1)
    #modelscolgrpdf=modelscoldf.groupby(['year','AIRLINE'],as_index=False).count().rename(columns={'ID':'ModelCount'})
    

    db=cloudMClnt['Aircraft']
    colmodelscloud=db['models']
    modelscoldf = pd.DataFrame(list(colmodelscloud.find().sort([('ID', 1)])))
    modelscoldf["month"]=modelscoldf["DATEOFORDER"].dt.month
    modelscoldf["year"]=modelscoldf["DATEOFORDER"].dt.year
    modelscoldf= modelscoldf.drop(['_id','MODEL_NO','DIMAID','WID','AIRCRAFT_TYPE','REGISTRATION','DESCRIPTION','SIZE','PRICE','SHIPPING','TAX','COMPANY','ORDEREDFROM','DATEOFORDER','PictureID','HangarClub'],axis=1)
    dummydf=createdummy(modelscoldf)
    modelscoldf2=pd.concat([modelscoldf,dummydf],ignore_index=True)
    
    modelscolgrpdf=modelscoldf2.groupby(['year','AIRLINE'],as_index=False).count().rename(columns={'ID':'ModelCount'})
    modelscolgrpdf['ModelCount']=modelscolgrpdf['ModelCount']-1


    uniqueAir = modelscolgrpdf['AIRLINE'].unique()
    #uniqueAir
    testdf=pd.DataFrame()
    lsttest=[]

    collairdf=pd.DataFrame()
    for airline in uniqueAir:
        #print(airline)
        testdict1={}
        testdict2={}
        runcount=0
        newdf = modelscolgrpdf[(modelscolgrpdf.AIRLINE == airline)]
        newdf.sort_values(by=['year'],inplace=True)
    
        newdf["Rtot"]=newdf['ModelCount'].cumsum()
        collairdf=pd.concat([collairdf,newdf])
    #runcount=runcount+modelscolgrpdf['ModelCount']
        for index, row in newdf.iterrows():
            testdict2[row['year']]=row['Rtot']
    #print(testdict2)   
    #testdf.head()
    #testdf[airline]=pd.Series(testdict2)
        testdict1[airline]=testdict2
        lsttest.append(testdict1)
                                 
#newdf.head(10)
    lsttest
    return lsttest