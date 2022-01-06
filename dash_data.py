

import pandas as pd
from pymongo import MongoClient
from config import cloudM,cloudMpassword,sqluser,sqlpass,servername
cloudMClnt=MongoClient()
cloudclient=MongoClient("mongodb+srv://"+ cloudM + ":"
                       + cloudMpassword + "@cluster0-omshy.mongodb.net/test?retryWrites=true&w=majority")

db=cloudclient['Aircraft']
colmodelscloud=db['models']

def cloudM_R():
    db=cloudMClnt['Aircraft']
    colmodels=db['models']
    colmodels2=db['models2']
    colmodels3=db['modelsold']
    colmodels4=db['solddetails']
    
    modelsdf = pd.DataFrame(list(colmodels.find().sort([('ID', 1)])))
    modelsolddf = pd.DataFrame(list(colmodels3.find()))
    solddetailsdf = pd.DataFrame(list(colmodels4.find()))
    #modelsdf = pd.DataFrame(list(colmodels.find()))
    return modelsdf,modelsolddf,solddetailsdf

df,df2,df3 = cloudM_R()

def collection_summary():
    
     aggpipeline = [{ "$group": {"_id":"$AIRLINE","total": { "$sum": "$PRICE" },"myCount": { "$sum": 1 }}}]
     cursor1=colmodelscloud.aggregate(aggpipeline)
     netcount_costdf = pd.DataFrame(cursor1)
     netcount_costdf=netcount_costdf.rename(columns={'_id':'Airline'})
     netcount_costdf=netcount_costdf.sort_values(['myCount'],ascending = False)
     aggpipeline =[{ "$group": {"_id": 
                               {"Airline":"$AIRLINE",
                                "Size":"$SIZE"},
                                "total": { "$sum": "$PRICE" },"myCount": { "$sum": 1 }}}]
     cursor2=colmodelscloud.aggregate(aggpipeline)
     netcount_spl_costdf = pd.DataFrame(cursor2)
     netcount_spl_costdf=netcount_spl_costdf.rename(columns={'_id':'Airline'})
     netcount_spl_costdf=netcount_spl_costdf.sort_values(['myCount'],ascending = False)
     testdf=netcount_spl_costdf.Airline.dropna().apply(pd.Series)

     netcount_spl_costdf['Airline1']=testdf['Airline']
     netcount_spl_costdf['Size']=testdf['Size']
     netcount_spl_costdf.drop('Airline',axis='columns', inplace=True)
     netcount_spl_costdf.rename(columns={'Airline1':'Airline'}, inplace = True)
     return netcount_costdf,netcount_spl_costdf