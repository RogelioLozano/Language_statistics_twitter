import os 
import gzip
import json
import random
import numpy as np
from itertools import repeat
max_tweets_Mex = 139400 # normalizados respecto a coyoacan i.e. 139400 es el num de tweets en coyo.
max_tweets_UK = 99903 # respecto a camden

# -1 corresponds to Mexico, 0 corresponds to CDMX and 1 to Coyoacan, the same with United kingdom but 0 is London and 1 is Camden

countries = ["Mexico", "United_Kingdom"]
Tweets_country = {"Mexico":max_tweets_Mex,"United_Kingdom":max_tweets_UK}
levels = [-1,0,1]

for country in countries:
    for admin_level in levels:

        if admin_level == -1:
            path = '/storage/gershenson_g/gershenson/Ranks_15-10-18/Filtrados'
            files = sorted(os.listdir(os.path.join(path,country,'')))
        else:
            path = os.path.join(os.getenv("HOME"),'Datos_correctos',country,'Level_{}'.format(admin_level),'')
            files = sorted(os.listdir(path))
        
        tamano = len(files)

        set_of_files_count = dict(zip(files,np.zeros(tamano)))
        empty_lists = [[] for i in repeat(None, tamano)]
        set_files = dict(zip(files,empty_lists))

        count = 0
        num_file = 0

        while count < Tweets_country[country]:
            file = files[num_file]
            num_file += 1
            set_of_files_count[file] += 1

            if num_file > (tamano-1):
                num_file = 0
            
            with gzip.open(os.path.join(path,file), 'r') as f:
                data = json.load(f)
                tweet = data[random.randint(0,len(data)-1)]
                
                if set_of_files_count[file] > 1:
                    if tweet not in set_files[file]:
                        set_files[file].append(tweet)
                        count += 1
                    else:
                        count += 0
                else:
                    set_files[file].append(tweet)
                    count += 1
                print('archivo:',file,"\n")
                print('Pais: ',country,'\n')
                print('Nivel: ',admin_level,'\n')
                print('Cuenta: ', count,'\n')
                print('Numero de tweets en el archivo:', len(set_files[file]))

        out_path = os.path.join(os.getenv("HOME"),'Datos_correctos','normalizados_conCoyo',country,'Level_{}'.format(admin_level),'')
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        for file in files:
            with gzip.open(os.path.join(out_path,file), 'wb') as g:
                set_files[file] = json.dumps(set_files[file])
                g.write(set_files[file].encode())