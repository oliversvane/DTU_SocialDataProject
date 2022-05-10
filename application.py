from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import app_config
from flask_bootstrap import Bootstrap
import json
from bokeh.embed import json_item
import plots.Folium_heat as heatmap
import pandas as pd
import pickle
import numpy as np


#Import of our definitions
import plots.barplots as SD_barblots
import plots.pieplot as SD_pieplot
import plots.Folium_heat as SD_heatmap
import plots.Folium_heat_time as SD_heatmap_time
from model.model import user_input_model


application = app = Flask(__name__)
app.config.from_object(app_config)
app.config['SECRET_KEY']='HC_Sutter'
Session(app)
Bootstrap(app)
#________________________________Support Functions___________________________________#
def get_data():
    return pd.read_pickle('data/data0705.pkl')

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
    state = request.args.get('state')
    print(state)
    if not state == "true":
        return json.dumps(json_item(SD_barblots.create_barplot(x_c,l_c,data), name))
    else:
        return json.dumps(json_item(SD_barblots.create_stacked_barplot(x_c,l_c,data), name))




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
    map = SD_heatmap_time.create_folium_heatmap_time("Year of construction",'Wgs84Latitude','Wgs84Longitude',data[data['Energy Label'].isin(x_c)])
    return map._repr_html_()



@app.route("/viz/viz5",methods=['GET'])
def viz5():
    name = "Barplot"
    data = get_data()
    return json.dumps(json_item(SD_barblots.create_barplot("Energy Label","Kommune",data), name))



#TODO Viz 6 - OLIVER
@app.route("/viz/viz6",methods=['GET'])
def viz6():
    x_cx = request.args.get('x_cx')
    x_c = request.args.get('x_c')
    data = get_data()

    map = SD_heatmap.create_folium_heatmap(data[data[x_cx]==x_c],"Wgs84Latitude","Wgs84Longitude",3,5)
    return map._repr_html_()


@app.route("/viz/viz7",methods=['GET'])
def viz7():
    name = "S_Barplot"
    data = get_data()
    return json.dumps(json_item(SD_barblots.create_stacked_barplot("Energy Label","Heat Supply",data), name))


@app.route("/viz/viz8",methods=['GET'])
def viz8():
    data = get_data()
    map = SD_heatmap.create_folium_area(data)
    return map._repr_html_()


@app.route("/model/predict",methods=['GET'])
def predict():
    input = request.args.get('input')
    input = input.split(',')
    inputX = [input[1],input[3],input[5],input[15],input[7],input[9],input[11],input[13],input[19],input[17]]
    model = pickle.load(open("model.pkl", 'rb'))
    scaler = pickle.load(open("scaler.pkl", 'rb'))
    
    pred = user_input_model(get_data(),inputX,scaler,model)

    print(pred[0])
    return pred[0]


@app.route("/api/unique",methods=['GET'])
def unique():
    name = request.args.get('name')
    data = list(np.sort(get_data()[name].unique()))
    data = [str(i) for i in data]
    return jsonify(data)




if __name__ == "__main__":
    app.run()
