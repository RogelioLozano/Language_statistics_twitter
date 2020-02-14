import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

number_of_ngrams=500

countries = ["United_Kingdom","Mexico"]
levels = [-1,0,1]

for country in countries:
    for admin_level in levels:

        file_location = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion','normalizados_region','Frequency_lists',country,'Level_{}'.format(admin_level),'')

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
                    try:
                        df=pd.read_csv(file_location+str(h)+'hourly/'+str(n)+'grams/'+str(m)+'.csv',sep='\t',names=['ngram','frequency'])
                    except FileNotFoundError:
                        continue
                
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

                path=file_location+'results_{}grams_pruebaunitaria/'.format(number_of_ngrams)
                if not os.path.exists(path):
                    os.makedirs(path)

                output_file = open(path+str(h)+'hour_'+str(n)+'grams_RD.txt','w')
                for n in range(number_of_ngrams):
                    str1=str(n+1)+'\t'+str(rank_diversity[n])
                    n=n+1
                    str1=str1+'\n' 
                    output_file.write(str1)
                output_file.close() 