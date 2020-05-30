import os 
import gzip
import json
import random
import numpy as np
from itertools import repeat
import pandas as pd

# This script normalize the number of tweets in all the buffers considered with the number of tweets in the buffer with radius of
# 3Km, this normalization is achieve selecting the aforementioned number of tweets randomly.

# countries = ["Mexico", "United_Kingdom","Spain","India"]
countries = ["Argentina"]

for country in countries:
    prein_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer',country,"")
    max_tweets = pd.read_csv( os.path.join(prein_path,"Dist_vs_numoftweets.csv") )
    max_tweets = max_tweets.Num_tweets[0]

    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),"South_Africa":np.arange(0,11),'Argentina':np.arange(0,11)}
    
    for admin_level in range(len(dist4country[country])):

        path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer',country,'Level_{}'.format(admin_level),'')
        file = os.listdir(path)
        datos = pd.read_csv(os.path.join(path,file[0]))
        datos = datos.sample(n=max_tweets)
        
        out_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer','normalizados_con3KM',country,'Level_{}'.format(admin_level),'3hourly_csv_files',"")
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        
        for ti in datos["Time Interval"].unique():
            towrite = datos[ datos["Time Interval"] == ti ]
            towrite = towrite[["Time Interval","Latitude","Longitude","Text"]]
            towrite.to_csv(  os.path.join( out_path ,"{}.csv".format(ti) ) ,index=False,sep="\t" )