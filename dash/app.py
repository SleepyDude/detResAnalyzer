from dash import Dash, html, dcc
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

fm = FilesManager()
data_dir = "C:/Projects/room/build-src-room-Desktop_Qt_5_15_0_MSVC2019_64bit-Release"
fm.readDirectory(data_dir)
detector_filenames = fm.getDetFiles()
# for df in detector_filenames:
#     print(df)
dm = DetectorManager()
for filename in detector_filenames:
    dm.appendResults(str(filename))

fig = go.Figure()

fig.update_xaxes(type="log")
fig.update_yaxes(type="log")

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

def addPlot(name):
    dm.detectors[name].mergeResults()
    res = dm.detectors[name].addit_results[0]
    res.calculateStatistics()

    x = res.BINS[res.bin_index]
    y = res.stat.means
    fig.add_trace(go.Scatter(
        x = x,
        y = y,
        line_shape='hv',
        name=name
    ))

if __name__ == "__main__":
    addPlot('Spec_Vert-1_SRC[100.00 keV]')
    addPlot('Spec_Vert-2_SRC[100.00 keV]')
    addPlot('Spec_Vert-3_SRC[100.00 keV]')
    addPlot('Spec_Vert-4_SRC[100.00 keV]')
    addPlot('Spec_Vert-5_SRC[100.00 keV]')
    addPlot('Spec_Vert-6_SRC[100.00 keV]')
    addPlot('Spec_Vert-7_SRC[100.00 keV]')
    addPlot('Spec_Vert-8_SRC[100.00 keV]')
    app.run_server(debug=True)