import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# reads at h hour aggrgated data and return 2h aggregated data

countries = ["Mexico"]
admins = {"Mexico":{-1:["Mexico"],0:["cdmx"], 1:["coyoacan","miguelhidalgo","iztapalapa"]}, "United_Kingdom":{-1:["United_Kingdom"],0:["london"], 1:["borough_of_camden"]}}
levels = [-1,0,1]

for country in countries:
    for admin_level in levels:
        for region in admins[country][admin_level]:
            # loop over the time scales in order
            for h in [3,6,12,24,48]:
                # file_location='../../../storage/gershenson_g/gershenson/Ranks_15-10-18/Filtrados/Frequency_lists/Normalize/'+country+'/'
                # file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Frequency_lists','Normalize',country,'Level_{}'.format(admin_level),'')
                # file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Countries','Frequency_lists','Normalize',country,'')
                
                if admin_level == -1:
                    file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Countries','iztapalapa_normalized','Frequency_lists','Normalize',country,'')
                else:
                    file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','iztapalapa_normalized','Frequency_lists','Normalize',country,'Level_{}_{}'.format(admin_level,region),'')

                files=os.listdir(file_location+str(h)+'hourly/1grams/')


                for m in range(int(len(files)/2)):
                    print(m,'of',int(len(files)/2))
                    for n in range(1,6):
                
                        df=pd.read_csv(file_location+str(h)+'hourly/'+str(n)+'grams/'+str(2*m)+'.csv',sep='\t',names=['ngram','frequency'])
                        # from the data frame create a list of words
                        ngrams=df['ngram'].tolist()
                        frequencies=df['frequency'].tolist()
                        
                        frequency_of={}
                        for i in range(len(ngrams)):
                            frequency_of[ngrams[i]]=frequencies[i]
                    
                        df2=pd.read_csv(file_location+str(h)+'hourly/'+str(n)+'grams/'+str(2*m+1)+'.csv',sep='\t',names=['ngram','frequency'])
                        ngrams=df2['ngram'].tolist()
                        frequencies=df2['frequency'].tolist()
                        
                        for i in range(len(ngrams)):        
                            if ngrams[i] in frequency_of:
                                frequency_of[ngrams[i]]=frequency_of[ngrams[i]]+frequencies[i]
                            else:
                                frequency_of[ngrams[i]]=frequencies[i]
                        
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
