import os 
import random
import numpy as np
import pandas as pd
import csv

countries = ["Mexico", "United_Kingdom"]
levels = [-1,0,1]

for country in countries:
    for admin_level in levels:

        path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion','normalizados_region',country,'Level_{}'.format(admin_level),'3hourly_csv_files','')
        files = os.listdir( os.path.join(path,'') )

        all_csvs = []
        for file in files:
            datos = pd.read_csv(os.path.join(path,file),sep='\t',quoting=csv.QUOTE_NONE)
            all_csvs.append(datos)

        alltweets = pd.concat(all_csvs,ignore_index=True)
        print(country,admin_level, "numero de tweets:",alltweets.shape)