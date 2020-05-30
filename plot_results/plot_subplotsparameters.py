import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.optimize import curve_fit
from copy import deepcopy
import os
import pandas as pd
import seaborn as sns
sns.set()
sns.set_style('ticks')

prepath = '/home/emmanuel/archivos_paragrafficar_SERVICIOSOCIAL/Buffers_Datosyprogramas/Datos_todoslosPaises/'

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


def mu_sigma_ngramsvar(fixed,country,ngrams,parametros,ax=None):
    """
    Input:
    fixed: str, 'scale' or 'time'
    ngrams: 1,2,3,4,5
    Parametros expect a pandas dataframe object.
    """
    #codigo auxiliar de distancia 
    # MODIFICAR SI AGREGAS MAS PAISES  <--------------___!!!!!!!!
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000
    
    if fixed == 'scale':
        #scale fixed (mu vs time interval)

        ax.plot(TIME,parametros.loc[ngrams],marker='o',label='ngrams={}'.format(ngrams))

    else:
        #time interval fixed (mu vs spatial scale)

        spatial_var = distancias
        ax.plot(spatial_var,parametros.loc[ngrams],marker='o',label='ngrams={}'.format(ngrams))
      
#------------------------------------------------------------------------------------


NGRAMS = [1,2,3,4,5]
TIME = [3,6,12,24,48,96]
#Modificar si cambio paises <--------------___!!!!!!!!
countries = ["Mexico", "United_Kingdom","Spain","Argentina"]
totalgrams = 1000
path = os.path.join(os.getenv("HOME"),'archivos_paragrafficar_SERVICIOSOCIAL','Buffers_Datosyprogramas','subplots_parameters')
sharey = True
sharex = False

for country in countries:
    # <--------------___!!!!!!!!
    #codigo auxiliar <--------------------Esto de abajo se tiene que modificar si aumentas paises 
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000
    SPATIAL = dist4country[country]

    #ngrams variation
    
    #geographical scale fixed
    subplots4country = {'Mexico':(4,3),'United_Kingdom':(4,3),'Spain':(3,3),'Argentina':(4,3)}
    nrows,ncols = subplots4country[country]
    fig1,ax1 = plt.subplots(nrows=nrows,ncols=ncols, figsize=(20,8),sharey=sharey,sharex=sharex)
    fig2,ax2 = plt.subplots(nrows=nrows,ncols=ncols, figsize=(20,8),sharey=sharey,sharex=sharex)
    fig1.text(0.5, 0.04, 'Temporal scale (hrs)',fontsize=20, ha='center')
    fig1.text(0.04, 0.5, '$\mu$',fontsize=20, va='center', rotation='vertical')
    fig2.text(0.5, 0.04, 'Temporal scale (hrs)',fontsize=20, ha='center')
    fig2.text(0.04, 0.5, '$\sigma$',fontsize=20, va='center', rotation='vertical')

    fig1.subplots_adjust(hspace = .7, wspace=.2)
    fig2.subplots_adjust(hspace = .7, wspace=.2)

    if country == 'Mexico':
        fig1.delaxes(ax1[3,2]); fig2.delaxes(ax2[3,2])
    elif country == 'United_Kingdom':
        fig1.delaxes(ax1[3,2]); fig2.delaxes(ax2[3,2])
        fig1.delaxes(ax1[3,1]); fig2.delaxes(ax2[3,1])
    elif country == 'Argentina':
        fig1.delaxes(ax1[3,2]); fig2.delaxes(ax2[3,2])

    ax1=ax1.ravel()
    ax2=ax2.ravel()
    for k,level in enumerate(SPATIAL):

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

        for ngram in NGRAMS:
            mu_sigma_ngramsvar('scale',country,ngram,df_mu,ax=ax1[k])
            ax1[k].set_title('{}Km'.format(distancias[level]/1000))
            ax1[k].set_xscale('log')
            ax1[k].grid()
            sns.despine(fig1,ax1[k])

        handles,labels=ax1[0].get_legend_handles_labels()
        fig1.legend(handles,labels,loc='upper right')

        saving_path=os.path.join(path,"{}ngrams".format(totalgrams),country,'displaying_ngrams','mu_vs_tempora')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig1.savefig(os.path.join(saving_path,'MUsubplotsdeKM'),format='pdf')
        plt.close()


        for ngram in NGRAMS:
            mu_sigma_ngramsvar('scale',country,ngram,df_sigma,ax=ax2[k])
            ax2[k].grid()
            ax2[k].set_xscale('log')
            ax2[k].set_title('{}Km'.format(distancias[level]/1000))  
            sns.despine(fig2,ax2[k])     

        handles,labels=ax2[0].get_legend_handles_labels()
        fig2.legend(handles,labels,loc='upper right')

        saving_path=os.path.join(path,"{}ngrams".format(totalgrams),country,'displaying_ngrams','sigma_vs_temporal')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig2.savefig(os.path.join(saving_path,'SIGMAsubplotsdeKM'),format='pdf')
        plt.close()
    
    #time interval fixed
    fig1,ax1 = plt.subplots(nrows=2,ncols=3, figsize=(20,8),sharey=sharey,sharex=sharex)
    fig2,ax2 = plt.subplots(nrows=2,ncols=3, figsize=(20,8),sharey=sharey,sharex=sharex)
    fig1.text(0.5, 0.04, 'Geographical scale (m)',fontsize=20, ha='center')
    fig1.text(0.04, 0.5, '$\mu$',fontsize=20, va='center', rotation='vertical')
    fig2.text(0.5, 0.04, 'Geographical scale (m)',fontsize=20, ha='center')
    fig2.text(0.04, 0.5, '$\sigma$',fontsize=20, va='center', rotation='vertical')
    fig1.subplots_adjust(hspace = .7, wspace=.2)
    fig2.subplots_adjust(hspace = .7, wspace=.2)

    ax1,ax2 = ax1.ravel(),ax2.ravel()
    for k,timeint in enumerate(TIME):

        tmpmu = dict( zip( dist4country[country], [[] for i in dist4country[country]] ) )
        tmpsigma = deepcopy(tmpmu)
        #MODIFICAR LO ABAJO SI AUEMNTO PAISES DEBO AGREGALOS A Parametros_sc  <--------------___!!!!!!!!
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
        
        for ngram in NGRAMS:
            mu_sigma_ngramsvar('time',country,ngram,df_mu,ax=ax1[k])
            ax1[k].set_xscale("log")
            ax1[k].set_title('{}hrs'.format(timeint))
            ax1[k].grid()
            sns.despine(fig1,ax1[k])
            
        handles,labels=ax1[0].get_legend_handles_labels()
        fig1.legend(handles,labels,loc='upper right')
        
        saving_path=os.path.join(path,'{}ngrams'.format(totalgrams),country,'displaying_ngrams','mu_vs_spatial')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig1.savefig(os.path.join(saving_path,'MUsubplotstime'),format='pdf')
        plt.close()

        for ngram in NGRAMS:
            mu_sigma_ngramsvar('time',country,ngram,df_sigma,ax=ax2[k])
            ax2[k].set_xscale("log")
            ax2[k].set_title('{}hrs'.format(timeint))
            ax2[k].grid()
            sns.despine(fig2,ax2[k])

        handles,labels=ax2[0].get_legend_handles_labels()
        fig2.legend(handles,labels,loc='upper right')

        saving_path=os.path.join(path,'{}ngrams'.format(totalgrams),country,'displaying_ngrams','sigma_vs_spatial')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig2.savefig(os.path.join(saving_path,'Sigmasubplotstime'),format='pdf')
        plt.close()