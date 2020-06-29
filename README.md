# Language statistics using geolocated twitter data.

In this project using proximity and regression analysis, around 18 million geolocated twitter data from four countries (Mexico, Spain, Argentina, and the United Kingdom) were analyzed to find out what can be said about:

+ The change in the use of language in different geographical, grammatical, and short time scales.
+ Which scale is the most important?

The metodology is based on a line of research related to rank dynamics of word usage (for example, see [rank dynamics](https://www.frontiersin.org/articles/10.3389/fphy.2018.00045/full) and [rank diversity](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0121898))

This project is part of the work that I did in my social service at Instituto de Investigaciones en Matemáticas Aplicadas y en Sistemas (IIMAS).


The [analysis notebook](https://github.com/RogelioLozano/Language_statistics_twitter/blob/master/stat_analysis/Analysis_notebook.ipynb) shows a summary of the statistical methods performed and plots of the results.


### Requirements:
Assuming that you already have a python3 scientific environment installed on your working station, you will need the following packages:
+ pandas >= 0.25.3
+ geopandas >= 0.6.1
+ numpy >= 1.17.3
+ matplotlib >= 3.1.1

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

In case you didn't want/have the twitter data, I submitted the relevant numerical data obtained through processing the twitter data in a folder called Datos_todoslosPaises. Run the scripts in the folder plot_results to see the rank diversity lognormal distribution for different temporal, spatial, and grammatical scales and the estimated parameters of those distributions. They will be saved in your home directory in a folder called "plots_RD".

To plot a linear regression of the estimated parameters, go to the folder "fitting_param". There execute the estimate_param.py script and the results will be saved in a folder called "parametros_valores" in your home directory. Finally, run fits_subplots.py located in the same folder as the last script. The fitted curves should be in "homedir/fitted_suplots".
