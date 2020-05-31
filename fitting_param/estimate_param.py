import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.optimize import curve_fit
from copy import deepcopy
import os
import pandas as pd
import seaborn as sns
sns.set(style='ticks')

prepath = 'Datos_todoslosPaises/'

def EvalnormCdf(x,mu,sigma):
    return scipy.stats.norm.cdf(np.log10(x),loc=mu,scale=sigma)

def ajuste(data_fit,funcion):
    X = data_fit[:,0]
    Y = data_fit[:,1]
    param_model, pcov1 = curve_fit(funcion,X,Y)
    return param_model

def get_parametros(country,level,ngrams,timeint,totalgrams):
    path = prepath+'{}/Level_{}/results_{}grams/{}hour_{}grams_RD.txt'.format(country,level,totalgrams,timeint,ngrams)
    data = np.loadtxt(path)
    parametros = ajuste(data,EvalnormCdf)
    return parametros

    
NGRAMS = [1,2,3,4,5]
TIME = [3,6,12,24,48,96]
countries = ["Mexico", "United_Kingdom","Spain","Argentina"]
totalgrams = 1000

pre = os.path.join(os.getenv("HOME"),'parametros_valores')

for country in countries:
    # <--------------___!!!!!!!!
    #codigo auxiliar <--------------------Esto de abajo se tiene que modificar si aumentas paises 
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000
    SPATIAL = dist4country[country]

    #ngrams variation
    
    #geographical scale fixed

    for level in SPATIAL:

        scheme = dict( zip( ['ti='+str(i) for i in TIME], [ [] for k in range(len(TIME)) ]) )
        muandsigma = {"mu":scheme, "sigma":deepcopy(scheme)}
        # <--------------___!!!!!!!!
        #Lo de abajo se debe aumentar acorde al numero de paises que se tengan entonces es el num de repeticiones en la lista de muandsigma
        Parametros_ti = dict([(count,elem) for count,elem in zip(countries,[muandsigma,muandsigma,muandsigma,muandsigma])])

        for timeint in TIME:
            for ngram in NGRAMS:
                try:
                    mu,sigma = get_parametros(country,level,ngram,timeint,totalgrams)
                except RuntimeError:
                    mu,sigma = np.nan,np.nan
                Parametros_ti[country]['mu']['ti={}'.format(timeint)].append(mu)
                Parametros_ti[country]['sigma']['ti={}'.format(timeint)].append(sigma)


        df_mu = pd.DataFrame(Parametros_ti[country]['mu'],index=NGRAMS)
        df_sigma = pd.DataFrame(Parametros_ti[country]['sigma'],index=NGRAMS)
        
        savingpathmu = os.path.join(pre,"{}ngrams".format(totalgrams),country,'display_ngrams','mu_vs_temporal')
        savingpathsigma = os.path.join(pre,'{}ngrams'.format(totalgrams),country,'display_ngrams','sigma_vs_temporal')
        
        if not os.path.exists(savingpathmu) or not os.path.exists(savingpathsigma):
            os.makedirs(savingpathmu)
            os.makedirs(savingpathsigma)
        df_mu.to_csv(os.path.join(savingpathmu,'{}Km'.format(distancias[level]/1000)))
        df_sigma.to_csv(os.path.join(savingpathsigma,'{}Km'.format(distancias[level]/1000)))
        
        
     # time interval fixed
    
    for timeint in TIME:
        tmpmu = dict( zip( dist4country[country], [[] for i in dist4country[country]] ) )
        tmpsigma = deepcopy(tmpmu)
        #MODIFICAR LO ABAJO SI AUEMNTO PAISES DEBO AGREGALOS A Parametros_sc  l<--------------___!!!!!!!!
        Parametros_sc = {"Mexico":{'mu':tmpmu ,'sigma':tmpsigma },  "United_Kingdom":{'mu':tmpmu ,'sigma':tmpsigma },'Spain':{'mu':tmpmu,'sigma':tmpsigma},'India':{'mu':tmpmu ,'sigma':tmpsigma },'Argentina':{'mu':tmpmu ,'sigma':tmpsigma}}
        for level in SPATIAL:
            for ngram in NGRAMS:
                try:
                    mu,sigma=get_parametros(country,level,ngram,timeint,totalgrams)
                except RuntimeError:
                    mu,sigma = np.nan,np.nan
                Parametros_sc[country]['mu'][level].append(mu)
                Parametros_sc[country]['sigma'][level].append(sigma)
            
        df_mu = pd.DataFrame({ str(distancia): Parametros_sc[country]["mu"][i] for(distancia,i) in zip( distancias,range(len(distancias))) },index=NGRAMS)
        df_sigma = pd.DataFrame({ str(distancia): Parametros_sc[country]["sigma"][i] for(distancia,i) in zip( distancias,range(len(distancias))) },index=NGRAMS)
        
        savingpathmu = os.path.join(pre,"{}ngrams".format(totalgrams),country,'display_ngrams','mu_vs_spatial')
        savingpathsigma = os.path.join(pre,'{}ngrams'.format(totalgrams),country,'display_ngrams','sigma_vs_spatial')
        
        if not os.path.exists(savingpathmu) or not os.path.exists(savingpathsigma):
            os.makedirs(savingpathmu)
            os.makedirs(savingpathsigma)
        df_mu.to_csv(os.path.join(savingpathmu,'{}hrs'.format(timeint)))
        df_sigma.to_csv(os.path.join(savingpathsigma,'{}hrs'.format(timeint)))
        