# Imports -- you may add others but do not need to
import plotly.plotly as py
import plotly.graph_objs as go
import csv
import plotly
import pandas as pd
from IPython.display import Image

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

plotly.tools.set_credentials_file(username='sangeethamg', api_key='8q2JvWWPxP1A31WMMw82')
py.sign_in('sangeethamg', '8q2JvWWPxP1A31WMMw82')

rawData = pd.read_csv('noun_data.csv')

data = [go.Bar(
            x=rawData['Noun'],
            y=rawData['Number'],
    )]

layout = go.Layout(title='Twitter - Noun Frequency', width=800, height=640)
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='part4_viz_image.png')

Image('part4_viz_image.png')
