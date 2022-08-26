from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from anadet.detectorManager import DetectorManager
from anadet.filesManager import FilesManager

app = Dash(__name__)

fig = go.Figure()

fig.update_xaxes(type="log")
fig.update_yaxes(type="log")

fig.update_layout(hovermode='x unified')

app.layout = html.Div(children=[
    html.H1(children="Hello Dash"),
    html.H6("Change the value"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='init value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),
    html.Div(children='''
        Dash: ???.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# test data
# for right plot with 'vh' line_shape we need to put [0] to the begin of 'y' list
y = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1] # len = 17
y = [0] + y
# bin i 0     1     2      3      4      5      6      7      8      9     10     11     12     13     14     15     16     17 
x = [1.23, 4.56, 7.89, 10.11, 12.13, 14.15, 16.17, 18.19, 20.21, 22.23, 24.25, 26.27, 28.29, 30.31, 32.33, 34.35, 36.37, 38.39] # len = 18
fig.add_trace(go.Scatter(
    x = x,
    y = y,
    line_shape='vh',
    name='test data'
))


# *** READ REAL DATA ***
# fm = FilesManager()
# data_dir = "C:/Projects/room/build-src-room-Desktop_Qt_5_15_0_MSVC2019_64bit-Release"
# fm.readDirectory(data_dir)
# detector_filenames = fm.getDetFiles()
# dm = DetectorManager()
# for filename in detector_filenames:
#     dm.appendResults(str(filename))

# def addPlot(name):
#     dm.detectors[name].mergeResults()
#     res = dm.detectors[name].addit_results[0]
#     res.calculateStatistics()

#     x = res.BINS[res.bin_index]
#     y = res.stat.means
#     fig.add_trace(go.Scatter(
#         x = x,
#         y = y,
#         line_shape='hv',
#         name=name
#     ))

if __name__ == "__main__":
    # addPlot('Spec_Vert-1_SRC[100.00 keV]')
    # addPlot('Spec_Vert-2_SRC[100.00 keV]')
    # addPlot('Spec_Vert-3_SRC[100.00 keV]')
    # addPlot('Spec_Vert-4_SRC[100.00 keV]')
    # addPlot('Spec_Vert-5_SRC[100.00 keV]')
    # addPlot('Spec_Vert-6_SRC[100.00 keV]')
    # addPlot('Spec_Vert-7_SRC[100.00 keV]')
    # addPlot('Spec_Vert-8_SRC[100.00 keV]')
    app.run_server(debug=True)