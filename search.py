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
