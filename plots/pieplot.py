from math import pi

import pandas as pd

from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
import bokeh.palettes  as palette # Pallete of colors

def create_pieplot(*_):
    
    x = {
        'No': 157,
        'Never': 93,
        'Nope': 63,
        'Negative': 54,
        'Difinetely Not': 44
    }

    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'answar'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = palette.magma(len(x))
    data['percent'] = ["{0:.0%}".format(x[i]/data['value'].sum()) for i in x]
    
    print(data)

    p = figure(height=350, title="Should you use a pie chart?", toolbar_location=None,
            tools="hover", tooltips="@answar: @percent", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='answar', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.sizing_mode = 'scale_both'

    return p