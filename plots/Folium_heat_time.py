import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap
from collections import defaultdict


#Default map of copenhagen
#Wgs84Longitude
#Wgs84Latitude

#Years = column with time stamp in years
#Lat = String column name
#Long String column name
#df = input data


def create_folium_heatmap_time(year_column,lat,long,df):
    years=sorted(list(df[year_column].unique()))
    map_data=[[[row[lat],row[long]] for index, row in df[df[year_column]==i].iterrows()] for i in years]
    cop_map = folium.Map([55.676098,12.568337], zoom_start=11)
    hm = plugins.HeatMapWithTime(map_data,
                                auto_play=True,
                                index=years,
                                max_opacity=0.8)
    hm.add_to(cop_map)
    return cop_map

