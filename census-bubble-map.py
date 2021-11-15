import plotly.graph_objects as go
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Draw a bubble map from processed data')
parser.add_argument('input', metavar='I', help='input file')
parser.add_argument('type')
args = parser.parse_args()

df = pd.read_csv(args.input)
df.head()

df['text'] = df['name'] + '<br>Population ' + (df['pop']).astype(str)
limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
cities = []
scale = 20

fig = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['pop']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))

fig.update_layout(
    title_text = '2020 US Taiwanese Census by ' + args.type + '<br>(Click legend to toggle traces)',
    showlegend = True,
    geo = dict(
        scope = 'usa',
        landcolor = 'rgb(217, 217, 217)',
    )
)

fig.show()
