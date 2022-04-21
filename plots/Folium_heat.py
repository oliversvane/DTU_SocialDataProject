import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap


#Default map of copenhagen
cop_map = folium.Map([55.676098,12.568337], zoom_start=11)
#Wgs84Longitude
#Wgs84Latitude

#Input
def create_folium_heatmap(df,lat,lon):
    heat_data = [lat,long for index, row in df.iterrows()]
    HeatMap(heat_data,blur=5,radius=20).add_to(cop_map)
    return cop_map
    