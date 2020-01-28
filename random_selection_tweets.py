import os 
import gzip
import json
import random
import numpy as np
from itertools import repeat
import pandas as pd

max_tweets_Mex = 139400 # normalizados respecto a coyoacan i.e. 139400 es el num de tweets en coyo.
max_tweets_UK = 99903 # respecto a camden

# -1 corresponds to Mexico, 0 corresponds to CDMX and 1 to Coyoacan, the same with United kingdom but 0 is London and 1 is Camden

# ARREGLAR EL SCRIPT, ES EL SIGUIENTE PARA EJECUTARSE!

countries = ["Mexico", "United_Kingdom"]
Tweets_country = {"Mexico":max_tweets_Mex,"United_Kingdom":max_tweets_UK}
levels = [-1,0,1]

for country in countries:
    for admin_level in levels:

        path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion','Formatted_data',country,'Level_{}'.format(admin_level),'3hourly_csv_files','')
        files = os.listdir( os.path.join(path,'') )
        for file in files:
            datos = pd.read_csv(os.path.join(path,file))
            datos = datos.sample(n=Tweets_country[country])
            
            out_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion','normalizados_region',country,'Level_{}'.format(admin_level),'3hourly_csv_files',"")
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            
            datos.to_csv(  os.path.join( out_path ,file ) ,index=False,sep="\t" )