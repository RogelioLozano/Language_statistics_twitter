import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error,r2_score
import seaborn as sns
sns.set(style='ticks')

def muVSnumtweets(vscale,value,country,level,ngrams,timeint,parametros,marker='o',ax=None):
    """
    Input:
    vscale: str, 'spatial' or 'time'
    value: str, 'mu' or 'sigma'
    Parametros expect a pandas dataframe object.
    """
    #codigo auxiliar de distancia 
    # MODIFICAR SI AGREGAS MAS PAISES  <--------------___!!!!!!!!
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000
        
    TIME = [3,6,12,24,48,96]
    
    if vscale == 'time':
        #scale fixed (mu vs time interval)
                
        ax.scatter(TIME,parametros.loc[ngrams],marker=marker,label='ng={}'.format(ngrams))

            
    else:
        #time interval fixed (mu vs spatial scale)

        spatial_var = distancias
        ax.scatter(spatial_var,parametros.loc[ngrams],marker=marker,label='ng={}'.format(ngrams))


def plot_paramet(vscale,param,country,ngram,timeint,ax,marker='o',level=None):
    """param: "mu" or "sigma" (string)
    vscale: versus what scale: "spatial", "temporal" (string) 
    level:0,1,2,3,4,5,6,7,8,9 (geographical level of buffer)
    ngrams: 1,2,3,4,5
    timeint: 3,6,12,24,48,96"""

    inputpath = os.path.join(os.getenv("HOME"),'archivos_paragrafficar_SERVICIOSOCIAL','Buffers_Datosyprogramas','curveFit_parametros','parametros_valores/1000ngrams/',country,'display_ngrams',f'{param}_vs_{vscale}')
    
    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000
    
    if vscale == "spatial":
        data = pd.read_csv( os.path.join(inputpath,f'{timeint}hrs'),index_col=0)
    else:
        data = pd.read_csv( os.path.join(inputpath,f'{distancias[level]/1000}Km'),index_col=0 )
    
    muVSnumtweets(vscale,param,country,level,ngram,timeint,data,marker,ax)
    
    return data

def regression_param(df,ax):
    """Plot OLS and return residuals"""
    x=np.array(df.columns,dtype='float').reshape(-1,1)
    y=df.iloc[ngram-1,:] #mu values at row ngram-1 corresponding to a certain scale

    # Create linear regression object
    reg = linear_model.LinearRegression()

    # Train the model 
    reg.fit(np.log10(x),y)

    ypred = reg.predict(np.log10(x))

    ax.plot(x,ypred)
    # ax.plot(x,ypred,label=f'$R^2={r2_score(y,ypred):.2f}$, slope ={reg.coef_[0]:.2f}')
    return (r2_score(y,ypred),reg.coef_[0])

#SUBPLOTS FITS PARAMETERS MU VS DISTANCE---------------------------

NGRAMS = [1,2,3,4,5]
TIME = [3,6,12,24,48,96]
#Modificar si cambio paises <--------------___!!!!!!!!
countries = ["Mexico", "United_Kingdom","Spain","Argentina"]
totalgrams = 1000
path = os.path.join(os.getenv("HOME"),'archivos_paragrafficar_SERVICIOSOCIAL','Buffers_Datosyprogramas','curveFit_parametros','fitted_suplots')
sharey = True
sharex = False

for country in countries:

    #time interval fixed
    fig1,ax1 = plt.subplots(nrows=2,ncols=3, figsize=(20,10),sharey=sharey,sharex=sharex) 
    fig2,ax2 = plt.subplots(nrows=2,ncols=3, figsize=(20,10),sharey=sharey,sharex=sharex)
    fig1.subplots_adjust(hspace = .7, wspace=.2)
    fig2.subplots_adjust(hspace = .7, wspace=.2)

    ax1,ax2 = ax1.ravel(),ax2.ravel()
    for k,timeint in enumerate(TIME):

        #MUS--------------------------------

        saving_path=os.path.join(path,'{}ngrams'.format(totalgrams),country,'displaying_ngrams','mu_vs_spatial')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        
        #diffrente markers in plots
        markers = np.arange(4,10,1)
        
        #dict of metrics from regression
        metricasmu = {}
        for ngram in NGRAMS:
            df=plot_paramet('spatial','mu',country,ngram,timeint,ax=ax1[k],marker=markers[ngram])
            r2,slope = regression_param(df,ax1[k])
            ax1[k].set_title('{}hrs'.format(timeint))
            ax1[k].set_xscale('log')
            ax1[k].set_ylabel('$\mu$')
            sns.despine(fig1,ax1[k])


            metricasmu[ngram] = [r2,slope]
            #Save table of metrics
            df1 = pd.DataFrame(metricasmu,index=['R^2','slope'])
            df1.to_csv(os.path.join(saving_path,f'MUmetrics_ti_{timeint}.csv'))

        plt.tight_layout()
        ax1[4].set_xlabel('Geographical scale (m)')

        handles,labels=ax1[0].get_legend_handles_labels()
        fig1.legend(handles,labels,loc='upper right')

        # fig1.savefig(os.path.join(saving_path,'MUsubplotstime'),format='png')
        plt.close()

        #SIGMAS--------------------------------

        saving_path=os.path.join(path,'{}ngrams'.format(totalgrams),country,'displaying_ngrams','sigma_vs_spatial')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)

        metricassigma = {}
        for ngram in NGRAMS:
            df=plot_paramet('spatial','sigma',country,ngram,timeint,ax=ax2[k],marker=markers[ngram])
            r2,slope = regression_param(df,ax2[k])
            ax2[k].set_title('{}hrs'.format(timeint))
            ax2[k].set_xscale('log')
            ax2[k].set_ylabel('$\sigma$')
            sns.despine(fig2,ax2[k])


            metricassigma[ngram] = [r2,slope]
            #save table of metrics
            df2 = pd.DataFrame(metricassigma,index=['R^2','slope'])
            df2.to_csv(os.path.join(saving_path,f'Sigmametrics_ti_{timeint}.csv'))


        # Ajusto el esquema de subplots para que queden juntitos
        plt.tight_layout()
        # Se pone la etiqueta en el 4 axis porque ese esta en el medio abajo.
        ax2[4].set_xlabel('Geographical scale (m)')
        
        # Se usa la leyenda de un eje (0) para usar como legend de todo el plot
        handles,labels=ax2[0].get_legend_handles_labels()
        fig2.legend(handles,labels,loc='upper right')

        # fig2.savefig(os.path.join(saving_path,'Sigmasubplotstime'),format='png')
        plt.close()