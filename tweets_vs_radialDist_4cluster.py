import geopandas as gpd
import os, csv
import pandas as pd
import numpy as np
import shapely.geometry

#modify the next path to where is you data if you cloned the repository
partial_path =  "/storage/gershenson_g/gershenson/Ranks_15-10-18/Filtrados/Formatted_data" #data in cluster

countries = ["Mexico", "United_Kingdom","Spain","India","South_Africa","Argentina"]

def buffer_filter(center,data,distances):
    """
    Assumes center a tuple or list with coordinates of center of buffers (Longitude,Latitude) 
    in that order, data is a Dataframe with columns containing Longitude and Latitude data.
    distances an iterable with the radial distances in Km from which form the buffers.

    Returns two Dataframes, the first is the same as data but with an extra column which 
    assigns an identifier to each data point based on the buffer where it lies. The other 
    Dataframe has two columns: Distances in km and the corresponding number of tweets.
    """
    
    gdf_coordinates = gpd.GeoDataFrame(data,geometry = gpd.points_from_xy(data.Longitude,data.Latitude),crs={"init":"epsg:4326"})
    #defines World Azimuthal Equidistant projection.
    proj4_txt = "+proj=aeqd +lat_0="+str(center[1]) + " +lon_0=" + str(center[0]) + " +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs" 
    gdf_coordinates = gdf_coordinates.to_crs(proj4_txt)



    long = [center[0]]
    lat = [center[1]]
    coord_center = pd.DataFrame({"Longitude":long,"Latitude":lat})
    gdf_center = gpd.GeoDataFrame(coord_center,geometry = gpd.points_from_xy(coord_center.Longitude,coord_center.Latitude),crs={"init":"epsg:4326"})
    gdf_center = gdf_center.to_crs(proj4_txt)

    results = {}
    tweets = []
    for d in np.array(distances):
        buffer = gdf_center.geometry.buffer(distance=d) 
        my_union = buffer.geometry.unary_union
        inside = [my_union.contains(gdf_coordinates.iloc[i].geometry) for i in range(len(gdf_coordinates))]
        
        tweets_inside = data[inside]
        iden=[d]*len(tweets_inside)
        tweets_inside = tweets_inside.assign(identificador=iden)
        tweets.append(tweets_inside)
        results[d/1000] = sum(inside)

    return pd.concat(tweets),pd.DataFrame(data={"Distance(km)":list(results.keys()),"Num_tweets":list(results.values())})

centermex = (-99.133217,19.432777) #long,latitud 
centeruk = (-0.118092,51.509865) 
centerspain= (-3.70275,40.4183083)
centerindia=(77.216721,28.644800)
centersouthafrica=(18.423300,-33.918861)
centerargentina=(-58.3772300,-34.6131500)


Centros = {"Mexico":centermex ,"United_Kingdom":centeruk,"Spain":centerspain,"India":centerindia,"South_Africa":centersouthafrica,"Argentina":centerargentina}

for country in countries:
    path = os.path.join( partial_path, country, "3hourly_csv_files","")
    files = sorted(os.listdir(path))

    multi_dataframes = []

    for file in files:
        df = pd.read_csv(path+file,sep="\t",quoting=csv.QUOTE_NONE)
        multi_dataframes.append(df)


    all_data = pd.concat(multi_dataframes)
    all_data.reset_index(drop=True,inplace = True)

    dist4country = { "Mexico":np.arange(0,11), "United_Kingdom":np.arange(0,10),"Spain":np.arange(0,9),"India":np.arange(0,11),"South_Africa":np.arange(0,11),'Argentina':np.arange(0,11)}
    base=2
    distancias = np.power(base, dist4country[country]).astype(float)*3*1000 #definicion de distancias en m.

    result,distVSnum = buffer_filter(Centros[country],all_data,distancias)
    
    preout_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer',country,"")
    if not os.path.exists(preout_path):
        os.makedirs(preout_path)
    distVSnum.to_csv(os.path.join(preout_path,"Dist_vs_numoftweets.csv"),index=False)

    for admin_level in range(len(distancias)):    
        out_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporBuffer',country,'Level_{}'.format(admin_level),'')
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        towrite = result[result.identificador == distancias[admin_level]]
        towrite.to_csv(os.path.join(out_path,"dataframeOut.csv"), index=False) #Se guardan con el mismo nombre pero contiene diferentes datos en distintas carpetas 
        # se hace esto para conservar consistencia con el codigo que he hecho anteriormente.