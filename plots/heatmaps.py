# Init dependencies
import pandas as pd

from bokeh.embed import file_html


# Begin functions:

def create_heatmap(attribute,data):
    """
    Input:
        attribute : str
            A string containing the name of the attribute of which the bokeh will create tabs

        data : DataFrame
            A pandas dataframe containing all the data


    Returns:
        heatmap : bokeh.file_html()
            A bokeh heatmap converted to html
            Read more here: https://docs.bokeh.org/en/latest/docs/user_guide/embed.html
    """

    heatmap = None
    return heatmap