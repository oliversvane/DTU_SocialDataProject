import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap
from collections import defaultdict


#Default map of copenhagen
cop_map = folium.Map([55.676098,12.568337], zoom_start=11)
#Wgs84Longitude
#Wgs84Latitude

#Input
def create_folium_heatmap(df,lat,long,blur,radius):
    heat_data = [[row[lat],row[long]] for index, row in df.iterrows()]
    HeatMap(heat_data,blur=blur,radius=radius).add_to(cop_map)
    return cop_map