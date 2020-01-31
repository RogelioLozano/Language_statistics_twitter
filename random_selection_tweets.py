import os 
import gzip
import json
import random
import numpy as np
from itertools import repeat
import pandas as pd
import csv

max_tweets_Mex = 139400 # normalizados respecto a coyoacan i.e. 139400 es el num de tweets en coyo.
max_tweets_UK = 99903 # respecto a camden

# -1 corresponds to Mexico, 0 corresponds to CDMX and 1 to Coyoacan, the same with United kingdom but 0 is London and 1 is Camden

# ARREGLAR EL SCRIPT, ES EL SIGUIENTE PARA EJECUTARSE!

countries = ["Mexico", "United_Kingdom"]
Tweets_country = {"Mexico":max_tweets_Mex,"United_Kingdom":max_tweets_UK}
levels = [-1,0]

# Implementar una funcion que solo se ejecute una vez dentro del loop enumerate files
def onlyonce(firstTime = [],data,persample,residue):
    if (firstTime == []) and (data.shape[0] > (persample+residue)):
        firstTime.append('Not Empty')
        return True
    else:
        return False

for country in countries:
    for admin_level in levels:

        path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion','Formatted_data',country,'Level_{}'.format(admin_level),'3hourly_csv_files','')
        files = os.listdir( os.path.join(path,'') )

        all_csvs = []
        for file in files:
            datos = pd.read_csv(os.path.join(path,file),sep='\t',quoting=csv.QUOTE_NONE)
            all_csvs.append(datos)
        
        alltweets = pd.concat(all_csvs,ignore_index=True)
        alltweets = alltweets.sample(n=Tweets_country[country])

        

        for file in files:
            datos = pd.read_csv(os.path.join(path,file),sep='\t',quoting=csv.QUOTE_NONE)
            if not datos.empty:
                if onlyonce(data=datos,persample=persample,residue=residue):
                    datos = datos.sample(n=persample+residue)
                elif datos.shape[0]>persample:
                    datos = datos.sample(n=persample)
                else:


            out_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion','normalizados_region',country,'Level_{}'.format(admin_level),'3hourly_csv_files',"")
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            datos.to_csv(  os.path.join( out_path ,file ) ,index=False,sep="\t" )

