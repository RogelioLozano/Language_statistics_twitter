# Language statistics using geolocated twitter data.

In this project using proximity and regresion analysis around 18 million geolocated twitter data from three Spanish-speaking and one English-speaking countries (Mexico, Spain, Argentina and United Kingdom)  to find out what can be said about:

+ The change of the use of language in different geographical, grammatical and short time scales.
+ Which scale is the most important?

The metodology is based on a line of research related to rank dynamics of word usage (for example, see [rank dynamics](https://www.frontiersin.org/articles/10.3389/fphy.2018.00045/full) and [rank diversity](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0121898))

This project is part of the work that I did in my social service at Instituto de Investigaciones en Matemáticas Aplicadas y en Sistemas (IIMAS).

### Requirements:
Assuming that you already have a python3 scientific environment installed on your working station, you will need the following packages:
+ pandas
+ geopandas
+ numpy
+ matplotlib

### Intructions

If you want to reproduce the results the data can be shared on request. First, clone this repository to your local machine:

git clone https://github.com/RogelioLozano/Language_statistics_twitter.git

If you have the twitter data, execute in the following order the next scripts:

1. tweets_vs_radialDist_4cluster.py
2. random_selection_tweets.py
3. tweets_to_ngram.py
4. aggregator.py
5. rank_diversity_v2.py 

The processed data with the rank diversity measures will be saved in your home directory in a folder called "Datos_correctos".

In case that you didn't want/have the twitter data, I submited the relevant numerical data obtained through processing the twitter data in a folder called Datos_todoslosPaises.




The [analysis notebook] shows the statistical methods performed and plots of the results. Here I show a sample of geolocated twitter data that belongs to a construcuted buffer as an example of the proximity analysis used in this project.
