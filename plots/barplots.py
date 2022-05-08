# Init dependencies
import pandas as pd
import numpy as np

# Bokeh import
from bokeh.plotting import figure
import bokeh.palettes  as palette # Pallete of colors
from bokeh.models import HoverTool,Range1d,NumeralTickFormatter
import warnings
import math


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

    x=data.groupby([attribute_y,attribute_x]).size().unstack(fill_value=0).to_dict('index')
    dict_data={}
    y_cat_list = []


    for i in list(x):
        y_cat_list.append(i)
        x_cat_list=[]
        temp_list = []
        for j in list(x[i]):
            value = x[i][j]        
            temp_list.append(value)
            x_cat_list.append(j)

        dict_data[i]=temp_list
    dict_data[attribute_x]=x_cat_list



    p = figure(x_range=x_cat_list, title=attribute_x + " over " + attribute_y,toolbar_location='below', tools="pan,wheel_zoom,box_zoom,reset", plot_height=500,plot_width=1000)
    p.sizing_mode = 'scale_width'
    colors =palette.turbo(len(y_cat_list))
    
    renderers = p.vbar_stack(y_cat_list, x=attribute_x, width=0.9, color=colors, source=dict_data,
                legend_label=y_cat_list,name=y_cat_list,line_color = None)


    for r in renderers:
        hover = HoverTool(tooltips=[
            ("Count", "@$name"),
            ("label","$name")
        ], renderers=[r],toggleable=False)
        p.add_tools(hover)
    p.xaxis.major_label_orientation = math.pi*2/7
    #p.xaxis.major_label_orientation = "vertical"
    p.title.text_font_size = '20pt'
    p.add_layout(p.legend[0], 'right')
    p.xaxis.axis_label = attribute_x
    p.yaxis.axis_label = attribute_y
    p.yaxis.formatter=NumeralTickFormatter(format="00")

    barplot = p
    return barplot

def create_stacked_barplot(attribute_x,attribute_y,data):
    """
    Input:
        attribute_x : str
            A string containing the name of the x-axis attribute
            
        attribute_y : str
            A string containing the name of the x-axis attribute
            
        data : DataFrame
            A pandas dataframe containing all the data


    Returns:
        barplot : bokeh plot
            A bokeh stacked barplot ready to be converted to html
            Read more here: https://docs.bokeh.org/en/latest/docs/user_guide/embed.html
    """
    x=data.groupby([attribute_y,attribute_x]).size().unstack(fill_value=0).to_dict('index')
    dict_data={}
    y_cat_list = []
    devide_list = [0 for i in list(x[list(x)[0]])]


    for i in list(x):
        y_cat_list.append(i)
        x_cat_list=[]
        temp_list = []
        for index,j in enumerate(list(x[i])):
            devide_list[index]=devide_list[index]+x[i][j]
            value = x[i][j]        
            temp_list.append(value)
            
            x_cat_list.append(j)

        dict_data[i]=temp_list
    dict_data[attribute_x]=x_cat_list


    for i in list(x):
        temp_list = []
        for index,j in enumerate(dict_data[i]):
            temp_list.append(j/devide_list[index])
        dict_data[i]=temp_list


    p = figure(x_range=x_cat_list, title=attribute_x + " over " + attribute_y,toolbar_location='below', tools="pan,wheel_zoom,box_zoom,reset",y_range=Range1d(bounds=(0, 1)), plot_height=500,plot_width=1000)
    p.sizing_mode = 'scale_width'
    colors =palette.turbo(len(y_cat_list))
    
    renderers = p.vbar_stack(y_cat_list, x=attribute_x, width=0.9, color=colors, source=dict_data,
                legend_label=y_cat_list,name=y_cat_list,line_color = None)


    for r in renderers:
        hover = HoverTool(tooltips=[
            ("percentage", "@$name{2 %}"),
            ("label","$name")
        ], renderers=[r],toggleable=False)
        p.add_tools(hover)

    p.title.text_font_size = '20pt'
    p.add_layout(p.legend[0], 'right')
    p.xaxis.axis_label = attribute_x
    p.yaxis.axis_label = attribute_y
    p.yaxis.formatter=NumeralTickFormatter(format="00")
    stacked_barplot = p
    return stacked_barplot

def create_histogram(title, attribute_x,data,bins=100):
    """
    Input:
        attribute_x : list
            A list containing the names of the x-axis attributes as strings
            
        data : DataFrame
            A pandas dataframe containing all the data


    Returns:
        barplot : bokeh plot
            A bokeh stacked barplot ready to be converted to html
            Read more here: https://docs.bokeh.org/en/latest/docs/user_guide/embed.html
    """
    p = figure(title=title, background_fill_color="#fafafa",toolbar_location='below', tools="pan,wheel_zoom,box_zoom,reset", plot_height=500,plot_width=1000)
    colors =palette.turbo(len(attribute_x))
    max_v = 0
    for index,i in enumerate(attribute_x):
        try:
            hist, edges = np.histogram(np.array(data[i]), density=False, bins=bins)
            p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                fill_color=colors[index], alpha=0.5,legend_label=i)
            max_t_v = max(hist)
            if max_t_v>max_v:
                max_v=max_t_v
        except:
            warnings.warn(f"{i} is of type string and cannot be used to create histogram. Please select another attribute")
        

    p.title.text_font_size = '20pt'
    p.y_range = Range1d(0, int(max_v*1.1), bounds="auto")
    p.add_layout(p.legend[0], 'right')
    p.legend.background_fill_color = "#fefefe"
    p.yaxis.axis_label = 'Count'
    p.grid.grid_line_color="white"
    return p