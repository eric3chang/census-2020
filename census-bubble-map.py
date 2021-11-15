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
cities = []
scale = 20

fig = go.Figure()

df_large_cities = df[df['pop'] >= 10000]
df_large_remain = df[df['pop'] < 10000]
df_medium_cities = df_large_remain[df_large_remain['pop'] >= 1000]
df_medium_remain = df[df['pop'] < 1000]
df_small_cities = df_medium_remain[df_medium_remain['pop'] >= 100]
df_tiny_cities = df[df['pop'] < 100]


def add_graph(figure, df_sub, color, lower, upper):
    figure.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=df_sub['lon'],
        lat=df_sub['lat'],
        text=df_sub['text'],
        marker=dict(
            size=df_sub['pop'] / scale,
            color=color,
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area'
        ),
        name='{0} - {1}'.format(lower, upper)))


add_graph(fig, df_large_cities, "royalblue", 10000, 100000)
add_graph(fig, df_medium_cities, "crimson", 1000, 10000)
add_graph(fig, df_small_cities, "lightseagreen", 100, 1000)
add_graph(fig, df_tiny_cities, "orange", 0, 100)

fig.update_layout(
    title_text='2020 US Taiwanese Census by ' + args.type + '<br>(Click legend to toggle traces)',
    showlegend=True,
    geo=dict(
        scope='usa',
        landcolor='rgb(217, 217, 217)',
    )
)

fig.show()
