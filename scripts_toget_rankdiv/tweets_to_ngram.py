import pandas as pd
import os
import random
import numpy as np

number_tweets = 1200000

countries = ["Mexico", "United_Kingdom","Spain","India","Argentina"] 

dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),"South_Africa":np.arange(0,11),'Argentina':np.arange(0,11)}


for country in countries:
    for admin_level in range(len(dist4country[country])):
        path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer','normalizados_con3KM',country,'Level_{}'.format(admin_level))

        files = os.listdir( os.path.join(path,'3hourly_csv_files','') )
        # find the earliest time for which there is data
        first=min([int(file[0:file.find('.')]) for file in files])

        random.shuffle(files)

        count = 0

        if (count <= number_tweets):

            for file in files:
            
                print(file)

        
                # PART 0 - Read the data and get a list of tweets that you want to examine
        
                # read the data as a dataframe
                # df=pd.read_csv(path+'Formatted_data/'+country+'/3hourly_csv_files/'+file,sep='\t',quoting=3)
                df = pd.read_csv(os.path.join(path,'3hourly_csv_files', file), sep='\t',quoting=3)
        
                #get the tweets
                tweets=df['Text'].tolist()
        

                # PART 1 - Read each tweet and identify phrases separated by punctuation
        
                #This is a list of 'stop' characters - might need updating as we find more things that mark the end of a phrase
                punctuation=['.',',',';',':','"','(',')','[',']','{','}','¿','?','-','!','/','-']
        
                # we first create a list of phrases in the tweet
                phrases=[]

                if (count <= number_tweets):

                    for tweet in tweets:
                        tweet=str(tweet)
                        # get the individual tokens
                        words=tweet.split()
                        #print(tweet)
                        #the phrase is a list of words 
                        phrase=[]
                        #words=[]
                        new_phrase=False
                        while len(words)>0:
                            #pop the first word on the list
                            word=words.pop(0)
            
                            # if a new phrase has begun then save the old one    
                            if new_phrase==True:
                                phrases.append(phrase)
                                phrase=[]    
                            new_phrase=False
                
                            #remove any punctuation characters from the beginning
                            while word[0] in punctuation and word not in punctuation:
                                # remove the 0th character from the word 
                                word=word[1:len(word)]
                                #start a new phrase
                                new_phrase=True
            
                            # if a new phrase has begun then save the old one               
                            if new_phrase==True:
                                phrases.append(phrase)
                                phrase=[]
                            new_phrase=False
                
                            #remove any punctuation characters from the end
                            while word[len(word)-1] in punctuation and word not in punctuation:
                                #remove th last character from the word
                                word=word[0:len(word)-1]
                                #start a new phrase
                                new_phrase=True
                
                            # add word to phrase but not if it is a single puntuation character
                            if word not in punctuation:
                                # change all characters to lower case
                                phrase.append(word.lower())
            
                        # need to add the last phrase
                        phrases.append(phrase)
                        count += 1
                
                # PART 2 - Take each phrase and count the 1, 2, 3 ,4 and 5 grams    
            
                # create a dictionary of dictionaries so that grams[n] will be the dictionary for ngrams
                grams={1:{},2:{},3:{},4:{},5:{}}
        
                for phrase in phrases:
                    for n in grams:
                        # here we create the ngrams (a phrase of length k will contain exactly k-n+1 ngrams)
                        for i in range(len(phrase)-n+1):
                            # create the ngram one word at a time
                            ngram=''
                            for word in phrase[i:i+n]:
                                # insert "--" between each word of the ngram
                                ngram=ngram+word+'--'
                            # remove the final "--"
                            ngram=ngram[0:len(ngram)-2]
                            # update the frequencies 
                            if ngram in grams[n]:
                                grams[n][ngram]=grams[n][ngram]+1
                            else:
                                grams[n][ngram]=1
        
        
                # PART 3 - Write the results to file
        
                for n in grams:
                    frequencies=[]
                    for ngram in grams[n]:
                        frequencies.append([ngram,grams[n][ngram]])
            
                    # sort the list so that highest frequencies are on top
                    frequencies=sorted(frequencies,key=lambda item: item[1],reverse=True)
            

                    output_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer','normalizados_con3KM','Frequency_lists',country,'Level_{}'.format(admin_level),'3hourly',str(n)+'grams','')

                    if not os.path.exists(output_path):
                        os.makedirs(output_path)

                    filename=str(int(file[0:file.find('.')])-first)+'.csv'
                    output_file = open(output_path+filename,'w')
                
                    for f in frequencies:
                        ngram=f[0]
                        frequency=f[1]
                        str1=ngram+'\t'+str(frequency)
                        str1=str1+'\n'
                        output_file.write(str1)
                    output_file.close()    