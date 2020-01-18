import os 
import gzip
import json
import random
import numpy as np
from itertools import repeat
max_tweets_Mex = 139400 # normalizados respecto a coyoacan i.e. 139400 es el num de tweets en coyo.
max_tweets_UK = 99903

countries = ["Mexico", "United_Kingdom"]
Tweets_country = {"Mexico":max_tweets_Mex,"United_Kingdom":max_tweets_UK}
admins = {"Mexico":{0:["cdmx"], 1:["coyoacan","miguelhidalgo"]}, "United_Kingdom":{0:["london"], 1:["borough_of_camden"]}}
levels = [0,1]

for country in countries:

    pathC = '/storage/gershenson_g/gershenson/Ranks_15-10-18/Filtrados'
    filesC = sorted(os.listdir(os.path.join(pathC,country,'')))
    tamano = len(filesC)

    #dictionary key=file_name : value=integer to count if that file has already been considered
    set_of_filesC_count = dict(zip(filesC,np.zeros(tamano)))
    empty_lists = [[] for i in repeat(None, tamano)]
    set_filesC = dict(zip(filesC,empty_lists))

    count = 0
    num_file = 0

    while count < Tweets_country[country]:
        file = filesC[num_file]
        num_file += 1
        set_of_filesC_count[file] += 1

        if num_file > (tamano-1): #To transverse the list of files again if count has't reached Tweets_country 
            num_file = 0

        with gzip.open(os.path.join(pathC,country,file), 'r') as f:
            data = json.load(f)
            tweet = data[random.randint(0,len(data)-1)]

            if set_of_filesC_count[file] > 1:
                if tweet not in set_filesC[file]:
                    set_filesC[file].append(tweet)
                    count += 1
                else:
                    count += 0
            else:
                set_filesC[file].append(tweet)
                count += 1
            print('archivo:',file,"\n")
            print('Pais: ',country,'\n')
            print('Cuenta: ', count,'\n')
            print('Numero de tweets en el archivo:', len(set_filesC[file]))

    # out_pathC = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Countries',country,'')
    out_pathC = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','Countries','iztapalapa_normalized',country,'')

    if not os.path.exists(out_pathC):
        os.makedirs(out_pathC)  
    
    for file in filesC:
        with gzip.open(os.path.join(out_pathC,file), 'wb') as g:
            set_filesC[file] = json.dumps(set_filesC[file])
            g.write(set_filesC[file].encode())
    
    for admin_level in levels:
        for region in admins[country][admin_level]:

            pathR = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data',country,'Level_{}_{}'.format(admin_level,region),'')
            filesR = sorted(os.listdir(pathR))
            tamano = len(filesR)

            set_of_filesR_count = dict(zip(filesR,np.zeros(tamano)))
            empty_lists = [[] for i in repeat(None, tamano)]
            set_filesR = dict(zip(filesR,empty_lists))

            count = 0
            num_file = 0

            while count < Tweets_country[country]:
                file = filesR[num_file]
                num_file += 1
                set_of_filesR_count[file] += 1

                if num_file > (tamano-1):
                    num_file = 0
                
                with gzip.open(os.path.join(pathR,file), 'r') as f:
                    data = json.load(f)
                    tweet = data[random.randint(0,len(data)-1)]
                    
                    if set_of_filesR_count[file] > 1:
                        if tweet not in set_filesR[file]:
                            set_filesR[file].append(tweet)
                            count += 1
                        else:
                            count += 0
                    else:
                        set_filesR[file].append(tweet)
                        count += 1
                    print(file,"\n")
                    print('Region: ',region,'\n')
                    print('Cuenta: ', count,'\n')
                    print('Numero de tweets en el archivo:', len(set_filesR[file]))

            out_pathR = os.path.join(os.getenv("HOME"),'Adminlevel_filtered_data','normalized_case','iztapalapa_normalized',country,'Level_{}_{}'.format(admin_level,region),'')
            if not os.path.exists(out_pathR):
                os.makedirs(out_pathR)
            for file in filesR:
                with gzip.open(os.path.join(out_pathR,file), 'wb') as g:
                    set_filesR[file] = json.dumps(set_filesR[file])
                    g.write(set_filesR[file].encode())