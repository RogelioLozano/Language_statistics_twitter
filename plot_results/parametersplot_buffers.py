import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.optimize import curve_fit
from copy import deepcopy
import os
import pandas as pd
import seaborn as sns
sns.set()

prepath = '/home/emmanuel/archivos_paragrafficar_SERVICIOSOCIAL/Buffers_Datosyprogramas/Datos_todoslosPaises/'

#     ------------------------------------------------------------
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


def mu_sigma_ngramsvar(fixed,value,country,level,ngrams,timeint,parametros,ax=None):
    """
    Input:
    fixed: str, 'scale' or 'time'
    value: str, 'mu' or 'sigma'
    Parametros expect a pandas dataframe object.
    """
    #ngrams variation
    #codigo auxiliar de distancia 
    # MODIFICAR SI AGREGAS MAS PAISES  <--------------___!!!!!!!!
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000
    
    if fixed == 'scale':
        #scale fixed (mu vs time interval)
        ax.plot(TIME,parametros.loc[ngrams],marker='o',label='{},{}km,ng={}'.format(country,distancias[level]/1000,ngrams))
        ax.set_xlabel('Temporal scale (hrs)',fontsize=20)
#         ax.set_xticks(TIME)  # si quiero mostrar los tiempos exactos 3,6, 12hrs etc en el eje x
        if value == 'mu':
            ax.set_ylabel('$\mu$',fontsize=20)
        else:
            ax.set_ylabel('$\sigma$',fontsize=20)
        ax.set_xscale('log')
    else:
        #time interval fixed (mu vs spatial scale)

        spatial_var = distancias
        ax.plot(spatial_var,parametros.loc[ngrams],marker='o',label='$\delta t$={},ng={}'.format(timeint,ngrams))
        ax.set_xlabel('Geographical scale (m)',fontsize=20)
#         ax.set_xticks(TIME)
        if value == 'mu':
            ax.set_ylabel('$\mu$',fontsize=20)
        else:
            ax.set_ylabel('$\sigma$',fontsize=20)
#------------------------------------------------------------------------------------

NGRAMS = [1,2,3,4,5]
TIME = [3,6,12,24,48,96]
#Modificar si cambio paises <--------------___!!!!!!!!
# countries = ["Mexico", "United_Kingdom","Spain","India","Argentina"]
countries = ["Argentina"]
totalgrams = 1200
path = os.path.join(os.getenv("HOME"),'archivos_paragrafficar_SERVICIOSOCIAL','Buffers_Datosyprogramas','parameters_plotBuffers')

for country in countries:
    # <--------------___!!!!!!!!
    #codigo auxiliar <--------------------Esto de abajo se tiene que modificar si aumentas paises 
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000
    SPATIAL = dist4country[country]

    # ngrams variation
    
    #scale fixed

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
        fig1,ax1 = plt.subplots(figsize=(10,7))
            
        for ngram in NGRAMS:
            mu_sigma_ngramsvar('scale','mu',country,level,ngram,timeint,df_mu,ax=ax1)
            ax1.legend()
            ax1.grid()
        
        saving_path=os.path.join(path,"{}ngrams".format(totalgrams),country,'displaying_ngrams','mu_vs_tempora')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig1.savefig(os.path.join(saving_path,'{}Km'.format(distancias[level]/1000)),format='pdf')
        plt.close()
        
        fig2,ax2 = plt.subplots(figsize=(10,7))
        for ngram in NGRAMS:
            mu_sigma_ngramsvar('scale','sigma',country,level,ngram,timeint,df_sigma,ax=ax2)
            ax2.legend()
            ax2.grid()
        
        saving_path=os.path.join(path,"{}ngrams".format(totalgrams),country,'displaying_ngrams','sigma_vs_temporal')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig2.savefig(os.path.join(saving_path,'{}Km'.format(distancias[level]/1000)),format='pdf')
        plt.close()
        
#     time interval fixed
    for timeint in TIME:
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
        
        fig1,ax1 = plt.subplots(figsize=(10,7))
        for ngram in NGRAMS:
            mu_sigma_ngramsvar('time','mu',country,level,ngram,timeint,df_mu,ax=ax1)
            ax1.legend()
            ax1.set_xscale("log")
            ax1.grid()
        
        saving_path=os.path.join(path,'{}ngrams'.format(totalgrams),country,'displaying_ngrams','mu_vs_spatial')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig1.savefig(os.path.join(saving_path,'{}hrs'.format(timeint)),format='pdf')
        plt.close()
        
        fig2,ax2 = plt.subplots(figsize=(10,7))
        for ngram in NGRAMS:
            mu_sigma_ngramsvar('time','sigma',country,level,ngram,timeint,df_sigma,ax=ax2)
            ax2.legend()
            ax2.set_xscale("log")
            ax2.grid()
        
        saving_path=os.path.join(path,'{}ngrams'.format(totalgrams),country,'displaying_ngrams','sigma_vs_spatial')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        fig2.savefig(os.path.join(saving_path,'{}hrs'.format(timeint)),format='pdf')
        plt.close()
            


