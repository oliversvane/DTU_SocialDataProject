from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import app_config
from flask_bootstrap import Bootstrap
import json
from bokeh.embed import json_item
import plots.Folium_heat as heatmap
import pandas as pd
import pickle


#Import of our definitions
import plots.barplots as SD_barblots
import plots.pieplot as SD_pieplot
import plots.Folium_heat as SD_heatmap
import plots.Folium_heat_time as SD_heatmap_time



application = app = Flask(__name__)
app.config.from_object(app_config)
app.config['SECRET_KEY']='HC_Sutter'
Session(app)
Bootstrap(app)
#________________________________Support Functions___________________________________#
def get_data():
    return pd.read_pickle('data/final_final_data.pkl')

#________________________________Main Page___________________________________________#
@app.route("/")
def index():
    return render_template('index.html')





@app.route("/map")
def map():
    data = get_data()
    heat_plot = heatmap.create_folium_heatmap(data,"Wgs84Latitude","Wgs84Longitude",2,1).save("map.html")
    return render_template("map.html")



@app.route("/map2")
def map2():
    data = pd.read_pickle('data/final_final_data.pkl')

    heat_plot = heatmap.create_folium_heatmap(data,"Wgs84Latitude","Wgs84Longitude",3,3).save("templates/map.html")

    return render_template('map.html')



#______________________________________VIZ Pages_______________________________________________#
@app.route("/viz/viz1",methods=['GET'])
def viz1():
    name = "Barplot"
    data = get_data()
    x_c = request.args.get('x_c')
    l_c = request.args.get('l_c')

    return json.dumps(json_item(SD_barblots.create_barplot(x_c,l_c,data), name))




@app.route("/viz/viz2",methods=['GET'])
def viz2():
    name = "Histogram"
    data = get_data()
    x_c = request.args.get('x_c')
    bins = request.args.get('bins')
    try:
        int(bins)
    except:
        bins=60
    
    return json.dumps(json_item(SD_barblots.create_histogram(f"Histogram showing distribution of {x_c}",[x_c],data,bins=int(bins)), name))






@app.route("/viz/viz4",methods=['GET'])
def viz4():
    data = get_data()
    x_c = request.args.get('x_c')
    x_c = [x for x in x_c]
    map = SD_heatmap_time.create_folium_heatmap_time("YearOfConstruction",'Wgs84Latitude','Wgs84Longitude',data[data['EnergyLabelClassification'].isin(x_c)])
    return map._repr_html_()



@app.route("/viz/viz5",methods=['GET'])
def viz5():
    name = "Barplot"
    data = get_data()
    return json.dumps(json_item(SD_barblots.create_barplot("EnergyLabelClassification","Kommune",data), name))



#TODO Viz 6



@app.route("/viz/viz7",methods=['GET'])
def viz7():
    name = "S_Barplot"
    data = get_data()
    return json.dumps(json_item(SD_barblots.create_stacked_barplot("EnergyLabelClassification","HeatSupply",data), name))




@app.route("/model/predict",methods=['GET'])
def predict():
    sewage = request.args.get('sewage')
    water = request.args.get('water')
    Cuse = request.args.get('Cuse')
    date = request.args.get('date')
    heat = request.args.get('heat')
    roof = request.args.get('roof')
    year = request.args.get('year')
    area = request.args.get('area')
    model = pickle.load(open("finalized_model", 'rb'))
    scaler = pickle.load(open("scaler", 'rb'))
    x = scaler.fit_transform([[sewage,water,Cuse,date,heat,roof,year,area]])
    pred = model.predict(x)

    

    return pred







if __name__ == "__main__":
    app.run()
