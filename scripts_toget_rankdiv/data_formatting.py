# this script reads twitter data in the form of a JSON file (with a name like 
# 20140101 i.e. 8 characters long and no file extension) and outputs a csv file
# with two columns: time inseconds since midnight Dec 31 2013, and the text of the tweet
# with all spaces added between emojis to make it easier to tokenize using "split"

# -1 corresponds to Mexico, 0 corresponds to CDMX and 1 to Coyoacan, the same with United kingdom but 0 is London and 1 is Camden

import time
import json
import os 
import gzip

countries = ["Mexico","United_Kingdom"]
levels = [-1,0,1]

for country in countries:
    for admin_level in levels:

        if admin_level == -1:
            path = os.path.join(os.getenv("HOME"),"..","..","storage","gershenson_g","gershenson","Ranks_15-10-18","Filtrados",country,'')
            files = sorted(os.listdir(path))
        else:
            path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion',country,'Level_{}'.format(admin_level),'')
            files = sorted(os.listdir(path))

        output_folder = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion','Formatted_data',country,'Level_{}'.format(admin_level),'')

        #files.remove('.DS_Store')

        n=0
        intervals=[]

        # format is [time interval,latitude,longitude,text]
        formatted_tweets=[]

        for file in files: 
            n=n+1
            print(n, file)
            # with open('../../../storage/gershenson_g/gershenson/Ranks_15-10-18/Filtrados/'+country+'/'+file, 'rb') as f:
            with open(os.path.join(path,file), 'rb') as f:
        
                g=gzip.open(f,'r')

                tweets=json.load(g)
            
                for i in range(len(tweets)):
                    tweet=tweets[i]
                    longitude=tweet['coordinates']['coordinates'][0]
                    latitude=tweet['coordinates']['coordinates'][1]
                
        
                    timestamp=tweet["created_at"]

                    time_end=len(timestamp)
                    timestamp=timestamp[4:time_end-10]+timestamp[time_end-4:time_end]

                    period=int(int(timestamp[7:9])/3)
                
                    timestamp=time.mktime(time.strptime(timestamp, "%b %d %H:%M:%S %Y"))-time.mktime(time.strptime('2016 Jan 1 00:00:00',"%Y %b %d %H:%M:%S"))

                    interval=int(timestamp/(60*60*3))
                    intervals.append(interval)
                
                    # repr makes sure the '\n' doesn't break the line
                    text=tweet["text"].encode('unicode_escape').decode('ASCII')
        
                    # put spaces between the emojis so they later get read as separate words
                    emoji_position=text.find('\\u')
                    while emoji_position>-1:
                        text=text[0:emoji_position]+' '+text[emoji_position:emoji_position+6]+' '+text[emoji_position+6:len(text)]
                        emoji_position=text.find('\\u',emoji_position+2)
            
                    emoji_position=text.find('\\U')
                    while emoji_position>-1:
                        text=text[0:emoji_position]+' '+text[emoji_position:emoji_position+10]+' '+text[emoji_position+10:len(text)]
                        emoji_position=text.find('\\U',emoji_position+2)
                
                    # remove \n and replace with space
                    return_position=text.find('\\n')
                    while return_position>-1:
                        text=text[0:return_position]+' '+text[return_position+2:len(text)]
                        return_position=text.find('\\n',return_position+1)
                
                    # remove \t and replace with space
                    tab_position=text.find('\\t')
                    while tab_position>-1:
                        text=text[0:tab_position]+' '+text[tab_position+2:len(text)]
                        tab_position=text.find('\\t',tab_position+1)
                
                    formatted_tweets.append([interval,latitude,longitude,text])
        
        interval_tweets={}
        for interval in range(min(intervals),1+max(intervals)):  
            interval_tweets[interval]=[]
        
        for tweet in formatted_tweets:
            interval=tweet[0]
            interval_tweets[interval].append(tweet)

        for interval in interval_tweets:   
            path = os.path.join( output_folder, '3hourly_csv_files', '')
            if not os.path.exists(path):
                os.makedirs(path)

            print(path+str(interval)+'.csv')
            output_file=open(path+str(interval)+'.csv','w')
            output_file.write('Time Interval\tLatitude\tLongitude\tText\n')

            for tweet in interval_tweets[interval]:
                interval=tweet[0]
                latitude=tweet[1]
                longitude=tweet[2]
                text=tweet[3]
                output_file.write(str(interval)+'\t'+str(latitude)+'\t'+str(longitude)+'\t'+text+'\n')
            output_file.close()
