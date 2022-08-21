from dash import Dash, html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Dash(__name__)

test_data = {}
y = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,0] # len = 18
# bin i                 0     1     2      3      4      5      6      7      8      9     10     11     12     13     14     15     16     17 
x = [1.23, 4.56, 7.89, 10.11, 12.13, 14.15, 16.17, 18.19, 20.21, 22.23, 24.25, 26.27, 28.29, 30.31, 132.33, 134.35, 136.37, 138.39] # len = 18

fig = go.Figure()
fig.add_trace(go.Scatter(
    x = x,
    y = y,
    line_shape='hv'
))

fig.update_layout(hovermode='x unified')

app.layout = html.Div(children=[
    html.H1(children="Hello Dash"),
    html.Div(children='''
        Dash: ???.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)