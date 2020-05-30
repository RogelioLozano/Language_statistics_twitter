import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.optimize import curve_fit
import os
import pandas as pd
from copy import deepcopy
from matplotlib.pyplot import cm

prepath = '/home/emmanuel/archivos_paragrafficar_SERVICIOSOCIAL/Buffers_Datosyprogramas/Datos_todoslosPaises/'

def EvalnormCdf(x,mu,sigma):
    return scipy.stats.norm.cdf(np.log10(x),loc=mu,scale=sigma)

def ajuste(data_fit,funcion):
    X = data_fit[:,0]
    Y = data_fit[:,1]
    param_model, pcov1 = curve_fit(funcion,X,Y)
    return param_model

def plotRD(country,level,ngrams,timeint,totalgrams,color,ax=None):
    """ Plot rank diversity using 4 different parameters 
    Input: 
    Country (str)<- Mexico,United_Kingdom
    level (int) <- (0,1,2,3,4,5,6,7,8,9,10)
    ngrams (int) <- (1,2,3,4,5)
    timeint (int) <- (3,6,12,24,48,96)
    """
    path = prepath+'{}/Level_{}/results_{}grams/{}hour_{}grams_RD.txt'.format(country,level,totalgrams,timeint,ngrams)
    # MODIFICAR SI AGREGAS MAS PAISES  <--------------___!!!!!!!!
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000 #definicion de distancias en km.
    data = np.loadtxt(path)
    
    if not ax:
        fig = plt.figure(figsize=(10,7))
        ax = fig.add_subplot(1,1,1)
        ax.set_title("{},{}Km,ngrams={},timeint={}".format(country,distancias[level]/1000,ngrams,timeint))
        ax.grid(which='both')

    ax.plot(data[:,0],data[:,1],c=color,label='{},{}Km,$\delta t$={},ng={}'.format(country,distancias[level]/1000,timeint,ngrams))
    ax.set_xlabel("$k$")
    ax.set_ylabel('d(k)')
    ax.set_xscale('log')

def plotnormCdfFit(country,level,ngrams,timeint,totalgrams,color,ax=None):
    path = prepath+'{}/Level_{}/results_{}grams/{}hour_{}grams_RD.txt'.format(country,level,totalgrams,timeint,ngrams)
    data = np.loadtxt(path)
    parametros = ajuste(data,EvalnormCdf)
    
    if not ax:
        fig = plt.figure(figsize=(10,7))
        ax = fig.add_subplot(1,1,1)
        ax.grid(which='both')
    ax.plot(data[:,0],EvalnormCdf(data[:,0],*parametros),'--',c=color,label="$\mu$={:.3},$\sigma$={:.3}".format(*parametros))
#     ax.plot(np.log10(data[:,0]),EvalnormCdf(data[:,0],*parametros),'--',label="$\mu$={:.3},$\sigma$={:.3}".format(*parametros))
    ax.set_xlabel("k")
    ax.set_ylabel('d(k)')
    ax.set_xscale('log')

NGRAMS = [1,2,3,4,5]
TIME = [3,6,12,24,48,96]
# AUMENTAR PAISES AQUI <--------------___!!!!!!!!
# countries = ["Mexico", "United_Kingdom","Spain","India"]
countries=['Argentina']

totalgrams = 1200
path = os.path.join(os.getenv("HOME"),'archivos_paragrafficar_SERVICIOSOCIAL','Buffers_Datosyprogramas','lognormalfit_plotsBuffers','{}grams'.format(totalgrams))

for country in countries:
    # MODIFICAR LO DE ABAJO SI AGREGAS PAISES  <--------------___!!!!!!!!
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    SPATIAL = dist4country[country]
    ##Displaying time variation
    for ngrams in NGRAMS:
        for level in SPATIAL:
            fig,ax = plt.subplots(figsize=(10,7))
            color = iter(cm.rainbow(np.linspace(0,1,len(TIME))))
            for t in TIME:
                c = next(color)
                plotRD(country,level,ngrams,t,ax=ax,totalgrams=totalgrams,color=c)
                try:
                    plotnormCdfFit(country,level,ngrams,t,totalgrams=totalgrams,ax=ax,color=c)
                except RuntimeError:
                    pass
            ax.grid(which="both")
            ax.legend()
            ax.set_title('Temporal variation',fontsize=20)
            
            #Codigo solo auxiliar para etiquetas de graficas que se guardan
            #MODIFICAR SI AGREGAS PAISES A LO DE ABAJO  <--------------___!!!!!!!!
            dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
            base=2
            distancias = np.power(base, dist4country[country]).astype(float)*3*1000
            
            saving_path=os.path.join(path,country,'displaying_time','{}grams'.format(ngrams))
            if not os.path.exists(saving_path):
                os.makedirs(saving_path)
            plt.savefig(os.path.join(saving_path,'{}Km'.format(distancias[level]/1000)),format='pdf')
            plt.close()
            
    ##Displaying ngrams variation
    
    for timeint in TIME:
        for level in SPATIAL:
            fig,ax = plt.subplots(figsize=(10,7))
            color = iter(cm.rainbow(np.linspace(0,1,len(NGRAMS))))
            for ngram in NGRAMS:
                c = next(color)
                plotRD(country,level,ngrams=ngram,timeint=timeint,ax=ax,totalgrams=totalgrams,color=c)
                try:
                    plotnormCdfFit(country,level,ngrams=ngram,timeint=timeint,totalgrams=totalgrams,ax=ax,color=c)
                except RuntimeError:
                    pass

            ax.grid(which="both")
            ax.legend()
            ax.set_title('Ngrams variation',fontsize=20)
            
            #codigo auxiliar de nuevo. MODIFICAR SI AGEGAS MAS PAISES  <--------------___!!!!!!!!
            dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
            base=2
            distancias = np.power(base, dist4country[country]).astype(float)*3*1000

            saving_path=os.path.join(path,country,'displaying_ngrams','{}hrs'.format(timeint))
            if not os.path.exists(saving_path):
                os.makedirs(saving_path)
            plt.savefig(os.path.join(saving_path,'{}Km'.format(distancias[level]/1000)),format='pdf')
            plt.close()
            
    #Displaying scale variation
    
    for ngrams in NGRAMS:
        for timeint in TIME:
            fig,ax = plt.subplots(figsize=(10,7))
            #PARA MEXICO
            color = iter(cm.rainbow(np.linspace(0,1,len(dist4country[country]) )))
            for level in range(len(dist4country[country])):
                c = next(color)
                plotRD(country=country,level=level,ngrams=ngrams,timeint=timeint,ax=ax,totalgrams=totalgrams,color=c)
                try:
                    plotnormCdfFit(country=country,level=level,ngrams=ngrams,timeint=timeint,totalgrams=totalgrams,ax=ax,color=c)
                except RuntimeError:
                    pass
                
            ax.grid(which="both")
            ax.legend()
            ax.set_title('Scale variation',fontsize=20)
                 
            saving_path=os.path.join(path,country,'displaying_scale','{}grams'.format(ngrams))
            if not os.path.exists(saving_path):
                os.makedirs(saving_path)
            plt.savefig(os.path.join(saving_path,'{}hrs'.format(timeint)),format='pdf')
            plt.close()