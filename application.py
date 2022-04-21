from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import app_config
from flask_bootstrap import Bootstrap
from bokeh.embed import file_html
from bokeh.resources import CDN

import plots.barplots as SD_barblots
import plots.heatmaps as SD_heatmaps



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
    plot_p = SD_barblots.create_stacked_barplot("buildingNature","conditionOfConstruction",data)
    plot = SD_barblots.create_barplot("buildingNature","conditionOfConstruction",data)
    return render_template('index.html',stacked_p_plot=file_html(plot_p, CDN, "stacked_p"),stacked_plot=file_html(plot, CDN, "stacked_p"))

if __name__ == "__main__":
    app.run()
