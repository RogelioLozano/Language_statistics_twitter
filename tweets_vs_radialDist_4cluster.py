import geopandas as gpd
import os, csv
import pandas as pd
import numpy as np
import shapely.geometry

path =  "/storage/gershenson_g/gershenson/Ranks_15-10-18/Filtrados/Formatted_data/Mexico/3hourly_csv_files/"

files = sorted(os.listdir(path))

Total_num_tweets = 0

multi_dataframes = []

for file in files:
    df = pd.read_csv(path+file,sep="\t",quoting=csv.QUOTE_NONE)
    Total_num_tweets += len(df)
    df = df[["Latitude","Longitude"]]
    multi_dataframes.append(df)

print("Total number of tweets:",Total_num_tweets)
print("--------------------------------------------------")
all_data = pd.concat(multi_dataframes)
all_data.reset_index(drop=True,inplace = True)

gdf_coordinates = gpd.GeoDataFrame(all_data,geometry = gpd.points_from_xy(all_data.Longitude,all_data.Latitude))
gdf_coordinates.crs = {"init":"epsg:4326"}

long = [-99.133217]
lat = [19.432777]
coord_zocalo = pd.DataFrame({"Longitude":long,"Latitude":lat})
gdf_zocalo = gpd.GeoDataFrame(coord_zocalo,geometry = gpd.points_from_xy(coord_zocalo.Longitude,coord_zocalo.Latitude))
gdf_zocalo.crs = {"init":"epsg:4326"}

distancias = [0.03,0.06,0.12,0.24,0.48,0.96,1.92,3.84,7.68,15.36,30.72]

results = {}
for d in distancias:
    buffer = gdf_zocalo.geometry.buffer(distance=d) 
    my_union = buffer.geometry.unary_union
    tweets_inside = [my_union.contains(gdf_coordinates.iloc[i].geometry) for i in range(len(gdf_coordinates))]
    results[d*100] = sum(tweets_inside)

results = pd.DataFrame(data={"Distance":list(results.keys()),"Num_tweets":list(results.values())})
print(results)