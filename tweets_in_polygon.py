"""
Filter tweets based on their location. Levels indicates the deepness of filtering of tweets to be done in terms of administrative
boundaries.
Input: gzip compressed JSON files. 
geojson files.
Output: filtered gzip compressed JSON files
"""

import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
import json
import os 
import gzip

data_path = os.path.join(os.getenv("HOME"),"..","..","storage","gershenson_g","gershenson","Ranks_15-10-18","Filtrados")
countries = ["Mexico", "United_Kingdom"]
admins = {"Mexico":["cdmx.geojson","coyoacan.geojson"], "United_Kingdom":["london.geojson","borough_of_camden.geojson"]}
levels = [0,1]


for country in countries:
    for admin_level in levels:

        poly_path = os.path.join(os.getenv("HOME"),'polygons',country+'_polygons') #get directory of polygons
        geopoly = admins[country][admin_level]

        files=sorted(os.listdir(os.path.join(data_path,country,'')))

        boundaries = gpd.read_file(os.path.join(poly_path,geopoly))
        boundaries_geo = boundaries.iloc[0]
        polygons = boundaries_geo["geometry"]

        for file in files: 
            with gzip.open(os.path.join(data_path,country,file), 'r') as f:
                data_filtered = []
                data = json.load(f)
                for tweet in data:
                    point = tweet['coordinates']['coordinates']
                    point = Point(point[0], point[1])
                    if polygons.contains(point):
                        data_filtered.append(tweet)
                #print(len(data))
                #print(len(data_filtered))
                out_path = os.path.join(os.getenv("HOME"),'Datos_correctos','Tweets_filtadosporRegion',country,'Level_{}'.format(admin_level),'')
                if not os.path.exists(out_path):
                    os.makedirs(out_path)

                if len(data_filtered) > 0:
                    with gzip.open(os.path.join(out_path,file), 'wb') as g:
                        data_filtered = json.dumps(data_filtered)
                        g.write(data_filtered.encode())

