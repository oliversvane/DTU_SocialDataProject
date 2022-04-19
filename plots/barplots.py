# Init dependencies
import pandas as pd

from bokeh.embed import file_html


# Begin functions:
def create_barplot(attribute_x,attribute_y,data):
    """
    Input:
        attribute_x : str
            A string containing the name of the x-axis attribute
            
        attribute_y : str
            A string containing the name of the x-axis attribute
            
        data : DataFrame
            A pandas dataframe containing all the data


    Returns:
        barplot : bokeh.file_html()
            A bokeh barplot converted to html
            Read more here: https://docs.bokeh.org/en/latest/docs/user_guide/embed.html
    """

    barplot = None
    return barplot