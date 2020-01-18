import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

number_of_ngrams=300

# countries = ["Mexico"]
# admins = {"Mexico":{-1:["Mexico"],0:["cdmx"], 1:["coyoacan","miguelhidalgo"]}, "United_Kingdom":{-1:["United_Kingdom"],0:["london"], 1:["borough_of_camden"]}}
# levels = [-1,0,1]


countries = ["Mexico"]
admins = {"Mexico":{-1:["Mexico"],0:["cdmx"], 1:["iztapalapa"]}, "United_Kingdom":{-1:["United_Kingdom"],0:["london"], 1:["borough_of_camden"]}}
levels = [1]

for country in countries:
    for admin_level in levels:
        for region in admins[country][admin_level]:

            # file_location='../../../storage/gershenson_g/gershenson/Ranks_15-10-18/Filtrados/Frequency_lists/Normalize/'+country+'/'
            # file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Frequency_lists','Normalize',country,'Level_{}'.format(admin_level),'')
            # file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Countries','Frequency_lists','Normalize',country,'')

            if admin_level == -1:
                    file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Countries','iztapalapa_normalized','Frequency_lists','Normalize',country,'')
            else:
                file_location = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','iztapalapa_normalized','Frequency_lists','Normalize',country,'Level_{}_{}'.format(admin_level,region),'')


            for h in [3,6,12,24,48,96]:
                if h == 3:
                    time_intervals = 2626
                elif h == 6:
                    time_intervals = 1313
                elif h == 12:
                    time_intervals = 656
                elif h == 24:
                    time_intervals = 328
                elif h == 48:
                    time_intervals = 164
                elif h == 96:
                    time_intervals = 82

                for n in range(1,6):
                    #print(h,n)
                    ngrams_at_rank=[[] for i in range(number_of_ngrams)]
                
                    number_of_days=0

                    for m in range(time_intervals):
                
                        df=pd.read_csv(file_location+str(h)+'hourly/'+str(n)+'grams/'+str(m)+'.csv',sep='\t',names=['ngram','frequency'])
                    
                        # from the data frame create a list of words
                        ngrams=df['ngram'].tolist()

                        if len(ngrams)>number_of_ngrams:
                            for r in range(number_of_ngrams):
                                ngram=ngrams[r]
                                ngrams_at_rank[r].append(ngram)
                            number_of_days = number_of_days + 1

                    if number_of_days != 0:
                        rank_diversity=[len(set(ngrams))/number_of_days for ngrams in ngrams_at_rank]
                    else:
                        rank_diversity=[0 for ngrams in ngrams_at_rank]

                    path=file_location+'results_{}grams/'.format(number_of_ngrams)
                    if not os.path.exists(path):
                        os.makedirs(path)

                    output_file = open(path+str(h)+'hour_'+str(n)+'grams_RD.txt','w')
                    for n in range(number_of_ngrams):
                        str1=str(n+1)+'\t'+str(rank_diversity[n])
                        n=n+1
                        str1=str1+'\n' 
                        output_file.write(str1)
                    output_file.close() 