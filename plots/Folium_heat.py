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
    scores = [4,3,2,1,-1,-2,-3,-4]
    map_data = pd.get_dummies(data[["Kommune","Energy Label"]],columns=['Energy Label'])
    map_data = map_data.groupby(["Kommune"]).sum().reset_index()
    score_list = []
    for row in map_data.iterrows():
        score = 0
        count = 0
        for i in range(len(row[1])):
            if not type(row[1][i]) == str:
                score += int(scores[i])*int(row[1][i])
                count += i
        score_list.append(score/count)
    map_data['score'] = score_list

    cop_map = folium.Map([55.676098,12.568337], zoom_start=11)
    f = open("data/geo_data.geojson", encoding='utf-8')
    test = json.load(f)
    f.close()
    for i in test['features']:
        print(i['properties']['label_dk'])
    
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
            s['properties']['Label_A'] = int(map_data[map_data['Kommune'] == kstr]['Energy Label_A'])
            s['properties']['Label_B'] = int(map_data[map_data['Kommune'] == kstr]['Energy Label_B'])
            s['properties']['Label_C'] = int(map_data[map_data['Kommune'] == kstr]['Energy Label_C'])
            s['properties']['Label_D'] = int(map_data[map_data['Kommune'] == kstr]['Energy Label_D'])
            s['properties']['Label_E'] = int(map_data[map_data['Kommune'] == kstr]['Energy Label_E'])
            s['properties']['Label_F'] = int(map_data[map_data['Kommune'] == kstr]['Energy Label_F'])
            s['properties']['Label_G'] = int(map_data[map_data['Kommune'] == kstr]['Energy Label_G'])
        except:
            print(kstr)
            s['properties']['Label_A'] = "Out of Scope"
            s['properties']['Label_B'] = "Out of Scope"
            s['properties']['Label_C'] = "Out of Scope"
            s['properties']['Label_D'] = "Out of Scope"
            s['properties']['Label_E'] = "Out of Scope"
            s['properties']['Label_F'] = "Out of Scope"
            s['properties']['Label_G'] = "Out of Scope"

    
    # and finally adding a tooltip/hover to the choropleth's geojson
    folium.GeoJsonTooltip(['Label_A', 'Label_B','Label_C', 'Label_D','Label_E', 'Label_F','Label_G']).add_to(cp.geojson)
    
    folium.LayerControl().add_to(cop_map)

    return cop_map