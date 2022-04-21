# Init dependencies
import pandas as pd

# Bokeh import
from bokeh.plotting import figure
import bokeh.palettes  as palette # Pallete of colors
from bokeh.models import HoverTool,Range1d

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



    p = figure(x_range=x_cat_list, title="Title Here",toolbar_location='above', tools="pan,wheel_zoom,box_zoom,reset")
    p.sizing_mode = 'scale_both'
    colors =palette.magma(len(y_cat_list))
    
    renderers = p.vbar_stack(y_cat_list, x=attribute_x, width=0.9, color=colors, source=dict_data,
                legend_label=y_cat_list,name=y_cat_list,line_color = None)


    for r in renderers:
        hover = HoverTool(tooltips=[
            ("Count", "@$name")
        ], renderers=[r],toggleable=False)
        p.add_tools(hover)


    p.add_layout(p.legend[0], 'below')

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


    p = figure(x_range=x_cat_list, title="Title Here",toolbar_location='above', tools="pan,wheel_zoom,box_zoom,reset",y_range=Range1d(bounds=(0, 1)))
    p.sizing_mode = 'scale_both'
    colors =palette.magma(len(y_cat_list))
    
    renderers = p.vbar_stack(y_cat_list, x=attribute_x, width=0.9, color=colors, source=dict_data,
                legend_label=y_cat_list,name=y_cat_list,line_color = None)


    for r in renderers:
        hover = HoverTool(tooltips=[
            ("percentage", "@$name{0 %}")
        ], renderers=[r],toggleable=False)
        p.add_tools(hover)


    p.add_layout(p.legend[0], 'below')
    stacked_barplot = p
    return stacked_barplot
