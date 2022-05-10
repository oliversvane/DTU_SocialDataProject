import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap
from collections import defaultdict
import json


#Default map of copenhagen
cop_map = folium.Map([55.676098,12.568337], zoom_start=11)
#Wgs84Longitude
#Wgs84Latitude

#Input
def create_folium_heatmap(df,lat,long,blur,radius):
    heat_data = [[row[lat],row[long]] for index, row in df.iterrows()]
    HeatMap(heat_data,blur=blur,radius=radius).add_to(cop_map)
    return cop_map



def create_folium_area(data):
    scores = [7,6,5,4,3,2,1,0]
    map_data = pd.get_dummies(data[["Kommune","Energy Label"]],columns=['Energy Label'])
    map_data = map_data.groupby(["Kommune"]).sum().reset_index()
    score_list = []
    for row in map_data.iterrows():
        score = 0
        count = 0
        for i in range(len(row[1])):
            if not type(row[1][i]) == str:
                score += int(scores[i])*int(row[1][i])
                count += row[1][i]
        score_list.append(score/count)
    map_data['score'] = score_list

    cop_map = folium.Map([55.676098,12.568337], zoom_start=11,height=500)
    f = open("data/geo_data.geojson", encoding='utf-8')
    test = json.load(f)
    f.close()

    cp = folium.Choropleth(
            geo_data=test,
            name="choropleth",
            data=map_data,
            columns=["Kommune", "score"],
            key_on="feature.properties.label_dk",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="",
            encoding = "utf-8-sig"
            ).add_to(cop_map)
    


    # looping thru the geojson object and adding a new property
    # and assigning a value from our dataframe
    for s in cp.geojson.data['features']:
        kstr = s['properties']['label_dk'] #.replace('Ã¸','ø').replace('Ã¥','å').replace('Ã†','æ').replace('Ã¦','æ')
        try: 
            s['properties']['Label_A'] = str(np.round((int(map_data[map_data['Kommune'] == kstr]['Energy Label_A']) / np.sum(map_data[map_data['Kommune'] == kstr]).values[1:].sum())*100,2))+" %"
            s['properties']['Label_B'] = str(np.round((int(map_data[map_data['Kommune'] == kstr]['Energy Label_B']) / np.sum(map_data[map_data['Kommune'] == kstr]).values[1:].sum())*100,2))+" %"
            s['properties']['Label_C'] = str(np.round((int(map_data[map_data['Kommune'] == kstr]['Energy Label_C']) / np.sum(map_data[map_data['Kommune'] == kstr]).values[1:].sum())*100,2))+" %"
            s['properties']['Label_D'] = str(np.round((int(map_data[map_data['Kommune'] == kstr]['Energy Label_D']) / np.sum(map_data[map_data['Kommune'] == kstr]).values[1:].sum())*100,2))+" %"
            s['properties']['Label_E'] = str(np.round((int(map_data[map_data['Kommune'] == kstr]['Energy Label_E']) / np.sum(map_data[map_data['Kommune'] == kstr]).values[1:].sum())*100,2))+" %"
            s['properties']['Label_F'] = str(np.round((int(map_data[map_data['Kommune'] == kstr]['Energy Label_F']) / np.sum(map_data[map_data['Kommune'] == kstr]).values[1:].sum())*100,2))+" %"
            s['properties']['Label_G'] = str(np.round((int(map_data[map_data['Kommune'] == kstr]['Energy Label_G']) / np.sum(map_data[map_data['Kommune'] == kstr]).values[1:].sum())*100,2))+" %"
        except:
            s['properties']['Label_A'] = "Out of Scope"
            s['properties']['Label_B'] = "Out of Scope"
            s['properties']['Label_C'] = "Out of Scope"
            s['properties']['Label_D'] = "Out of Scope"
            s['properties']['Label_E'] = "Out of Scope"
            s['properties']['Label_F'] = "Out of Scope"
            s['properties']['Label_G'] = "Out of Scope"

    
    # and finally adding a tooltip/hover to the choropleth's geojson
    folium.GeoJsonTooltip(['label_dk','Label_A', 'Label_B','Label_C', 'Label_D','Label_E', 'Label_F','Label_G']).add_to(cp.geojson)
    
    folium.LayerControl().add_to(cop_map)

    return cop_map