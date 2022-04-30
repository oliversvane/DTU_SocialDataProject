from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import app_config
from flask_bootstrap import Bootstrap
#from bokeh.embed import file_html
#from bokeh.resources import CDN

import plots.barplots as SD_barblots
import plots.Folium_heat as heatmap


## Temp imports:
import pandas as pd



application = app = Flask(__name__)
app.config.from_object(app_config)
app.config['SECRET_KEY']='HC_Sutter'
Session(app)
Bootstrap(app)


#________________________________Main Page___________________________________________#
@app.route("/")
def index():
    data = pd.read_pickle('data/final_final_data.pkl')
    plot_p = SD_barblots.create_stacked_barplot("Kommune","EnergyLabelClassification",data)
    plot = SD_barblots.create_barplot("Kommune","EnergyLabelClassification",data)
    heat_plot = heatmap.create_folium_heatmap(data,"Wgs84Latitude","Wgs84Longitude",2,1)

    return render_template('index.html'
    ,stacked_p_plot=file_html(plot_p, CDN, "stacked_p")
    ,stacked_plot=file_html(plot, CDN, "stacked_p")
    ,heat_plot=heat_plot)

@app.route("/map")
def map():
    data = pd.read_pickle('data/final_final_data.pkl')
    heat_plot = heatmap.create_folium_heatmap(data,"Wgs84Latitude","Wgs84Longitude",2,1).save("map.html")
    return render_template("map.html")



@app.route("/map")
def map():
    data = pd.read_pickle('data/final_final_data.pkl')

    heat_plot = heatmap.create_folium_heatmap(data,"Wgs84Latitude","Wgs84Longitude",3,3).save("templates/map.html")

    return render_template('map.html')

if __name__ == "__main__":
    app.run()
