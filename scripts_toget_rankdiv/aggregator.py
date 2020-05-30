import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# reads at h hour aggrgated data and return 2h aggregated data

countries = ["Mexico", "United_Kingdom","Spain","India","Argentina"]

dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),"South_Africa":np.arange(0,11),'Argentina':np.arange(0,11)}

for country in countries:
    for admin_level in range(len(dist4country[country])):
        # loop over the time scales in order
        for h in [3,6,12,24,48]:
            file_location = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer','normalizados_con3KM','Frequency_lists',country,'Level_{}'.format(admin_level),'')
            
            files=os.listdir(file_location+str(h)+'hourly/1grams/')

            maxcsv=max([int(file[0:file.find('.')]) for file in files])

            for m in range(int(maxcsv/2)+1):
                for n in range(1,6):
                    try:
                        df=pd.read_csv(file_location+str(h)+'hourly/'+str(n)+'grams/'+str(2*m)+'.csv',sep='\t',names=['ngram','frequency'])
                        ngrams=df['ngram'].tolist()
                        frequencies=df['frequency'].tolist()

                        frequency_of={}
                        for i in range(len(ngrams)):
                            frequency_of[ngrams[i]]=frequencies[i]
                        
                        flag = 1

                    except FileNotFoundError:
                        try:
                            df2=pd.read_csv(file_location+str(h)+'hourly/'+str(n)+'grams/'+str(2*m+1)+'.csv',sep='\t',names=['ngram','frequency'])
                            flag = 0
                        except FileNotFoundError:
                            continue
                    
                    try:
                        df2=pd.read_csv(file_location+str(h)+'hourly/'+str(n)+'grams/'+str(2*m+1)+'.csv',sep='\t',names=['ngram','frequency'])
                        ngrams=df2['ngram'].tolist()
                        frequencies=df2['frequency'].tolist()

                        if flag != 1:
                            frequency_of={}
                            for i in range(len(ngrams)):
                                frequency_of[ngrams[i]]=frequencies[i]
                        else:
                            for i in range(len(ngrams)):        
                                if ngrams[i] in frequency_of:
                                    frequency_of[ngrams[i]]=frequency_of[ngrams[i]]+frequencies[i]
                                else:
                                    frequency_of[ngrams[i]]=frequencies[i]
                    except FileNotFoundError:
                        pass
                    
                    frequencies=[]
                    for ngram in frequency_of:
                        frequencies.append([ngram,frequency_of[ngram]])
                    
                    # sort the list so that highest frequencies are on top
                    frequencies=sorted(frequencies,key=lambda item: item[1],reverse=True)
        
                    # create folders for the aggregated data
                    path=file_location+str(2*h)+'hourly/'+str(n)+'grams/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                
                    output_file = open(path+str(m)+'.csv','w')
                    
                    for f in frequencies:
                        ngram=f[0]
                        frequency=f[1]
                        str1=str(ngram)+'\t'+str(frequency)
                        str1=str1+'\n'
                        output_file.write(str1)
                    output_file.close()    # output should be h*2 hourly
