# Note that to install plotly using Microsoft Visual Studio...
# Open Python interactive window
# >>> import pip
# >>> pip.main(['install', 'plotly'])

import plotly.plotly as py
import plotly.graph_objs as go

import numpy

def generate_rainbow_colours(N):
    # Code from https://plot.ly/python/box-plots/
    # generate an array of rainbow colors by fixing the saturation and lightness of the HSL representation of colour 
    # and marching around the hue. 
    # Plotly accepts any CSS color format, see e.g. http://www.w3schools.com/cssref/css_colors_legal.asp.
    return ['hsl('+str(h)+',50%'+',50%)' for h in numpy.linspace(0, 360, N)]

def plot(original_data):
    n_boxes = len(original_data)
    colors = generate_rainbow_colours(n_boxes)

    data = [go.Box(
                y=box
            )
            for box in original_data
            ] 

    data = []
    for box in range(n_boxes):
        data.append(go.Box(
            y=original_data[box],
            name="Scenario" + str(box + 1),
            marker = dict(
                color = colors[box]
            )
        ))
    py.sign_in('cameronmcphail', 'Lr5cKgcxMbb7INeJmqNk')
    py.iplot(data)