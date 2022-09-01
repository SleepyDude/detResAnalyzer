from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from random import randint
import distinctipy

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from anadet.detectorManager import DetectorManager
from anadet.filesManager import FilesManager
from anadet.detector import Detector


# *** READ REAL DATA ***
fm = FilesManager()
data_dir = "C:/Projects/room/results"
fm.readDirectory(data_dir)
detector_filenames = fm.getDetFiles()
dm = DetectorManager()
for filename in detector_filenames:
    dm.appendResults(str(filename))

# prepare to take data from detectors
for _, det in dm.detectors.items():
    ch = det.prima_results[0].strip()
    ch = ch.shrinkToDelta(0.1)
    det.highlightResult(ch)

# DASH PART
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

colors = distinctipy.get_colors(40)
def gen_col():
    gen_col.i += 1
    if gen_col.i >= len(colors):
        gen_col.i = 0
    return colors[gen_col.i]
gen_col.i = 13

fig = go.Figure()
fig2 = go.Figure()
# fig3 = go.Figure()
# fig4 = go.Figure()
# fig5 = go.Figure()
# fig6 = go.Figure()

fig.update_xaxes(type="log")
fig.update_yaxes(type="log")

fig.update_layout(hovermode='x unified', height=800, )

# test_items = ['MeV', '1', 'keV', 'lol']

# app.layout = html.Div(children=[
#     dcc.Dropdown(
#         options=[{'label': i, 'value': i} for i in test_items],
#         value='Age',
#         id='dropdown',
#         style={"width": "50%", "offset":1,},
#         clearable=False,
#     ),
#     dcc.Graph(
#         id='first-graph',
#         figure=fig
#     )
# ])

# app.layout = html.Div(
#     children=[
#         html.Div(
#             children=[
#                 html.P(children="⚙️", className="header-emoji"),
#                 html.H1(children="Аналитика детекторов в помещении 100х50х10 метров", className="header-title",),
#                 html.P(
#                     children="Анализ зависимости спектра и углового распределения"
#                     " от детектора, его удаления от источника и от стен"
#                     " Источник расположен в углу комнаты на высоте 1.5 м. и на расстоянии 0.5 м. от стен",
#                     className="header-description",
#                 ),
#             ],
#             className="header",
#         )

#         dcc.Graph(
#             figure=fig
#         ),
#         dcc.Graph(
#             figure=fig2
#         ),
#     ]
# )

QUANTITIES = ['Spec', 'Phi', 'Theta']
TAGS = ['Vert', 'Diag', 'XWall', 'YWall']
ENERGY = ['1 MeV', '100 keV', '1 keV', '1 eV', 'All']
NUMS = {
    'Vert': 8,
    'Diag': 10,
    'XWall': 10,
    'YWall': 10
}

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="⚙️", className="header-emoji"),
                html.H1(
                    children="Аналитика Детекторов", className="header-title"
                ),
                html.P(
                    children="Анализ зависимости спектра и углового распределения"
                    " от детектора, его удаления от источника и от стен"
                    " Источник расположен в углу комнаты на высоте 1.5 м. и на расстоянии 0.5 м. от стен",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Quantity", className="menu-title"),
                        dcc.Dropdown(
                            id="quantity-filter",
                            options=[
                                {"label": quantity, "value": quantity}
                                for quantity in QUANTITIES
                            ],
                            value="Spec",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="tag-filter",
                            options=[
                                {"label": tag, "value": tag}
                                for tag in TAGS
                            ],
                            value="Vert",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Energy",
                            className="menu-title"
                            ),
                            dcc.Dropdown(
                                id="energy-filter",
                                options=[
                                    {"label": energy, "value": energy}
                                    for energy in ENERGY
                                ],
                                value="All",
                                clearable=False,
                                searchable=False,
                                className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children="Num",
                            className="menu-title-num menu-title"
                        ),
                        dcc.Dropdown(
                            id="num-filter",
                            options=[],
                            multi=True,
                            className="dropdown",
                            value='All'
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="...",
                            className="menu-title-num menu-title"
                        ),
                        html.Button(
                            'Plot', 
                            id='submit-plot', 
                            className='Select-control plot-btn',
                            n_clicks=0,
                        ),
                    ]
                ),
            ],
            className="menu-num",
        ),
        html.P(id='graph-title', children=[]),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="spec-chart",
                        figure=fig
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="theta-chart",
                        figure=fig2
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output('num-filter', 'options'),
    Input('tag-filter', 'value')
)
def update_num_filter(tag):
    options = [str(i) for i in range(1,NUMS[tag]+1)]
    options.append('All')
    return options

@app.callback(
    Output('spec-chart', 'figure'),
    Input('submit-plot', 'n_clicks'),
    State('quantity-filter', 'value'),
    State('tag-filter', 'value'),
    State('energy-filter', 'value'),
    State('num-filter', 'value'),
)
def plot_graph(n_clicks, quantity, tag, aenergy_string: str, anums):
    energies = []
    if aenergy_string == "All":
        energies = [i for i in ENERGY if i != "All"]
    else:
        energies.append(aenergy_string)
    
    nums = []
    if 'All' in anums:
        nums = [i for i in range(1, NUMS[tag]+1)]
    else:
        nums = [i for i in anums]

    dets = dm.filterQuantity(detectors, quantity)
    dets = dm.filterTag(dets, tag)
    for en in energies:
        En = float(en.split()[0])
        E_unit = en.split()[1]
        for num in nums:
            d = dm.filterEnergy(dets, En, E_unit)
            d = dm.filterNum(d, num)
            for keyname, value in d.items():
                _, det = value
                plotNormDetector(fig, det, keyname)
            
    return fig

def plotMeansDetector(fig: go.Figure, det: Detector, name: str):
    x, y, _, _ = det.get_means_hl()
    color = gen_col()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({color[0]},{color[1]},{color[2]})',
        name=name,
        line_shape='vh',
    ))

def plotNormDetector(fig: go.Figure, det: Detector, name: str):
    x, y, = det.get_norm_hl()
    color = gen_col()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({color[0]},{color[1]},{color[2]})',
        name=name,
        line_shape='vh',
    ))

def plotNormWidthDetector(fig: go.Figure, det: Detector, name: str):
    x, y, = det.get_norm_width_hl()
    color = gen_col()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({color[0]},{color[1]},{color[2]})',
        name=name,
        line_shape='vh',
    ))

def plotNormWidthTheta(fig: go.Figure, det: Detector, name: str):
    x, y, = det.get_norm_width_theta_hl()
    color = gen_col()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({color[0]},{color[1]},{color[2]})',
        name=name,
        line_shape='vh',
    ))

if __name__ == "__main__":
    detectors = dm.prep_dets_for_filtering(dm.detectors)
    app.run_server(debug=True)