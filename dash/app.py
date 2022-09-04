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

spec_fig = go.Figure()
phi_fig = go.Figure()
theta_fig = go.Figure()

spec_fig.update_layout(hovermode='x unified', height=800, )
phi_fig.update_layout(hovermode='x unified', height=800, )
theta_fig.update_layout(hovermode='x unified', height=800, )

spec_fig.update_xaxes(type="log")
spec_fig.update_yaxes(type="log")

phi_fig.update_yaxes(type="log")
theta_fig.update_yaxes(type="log")

spec_fig.update_xaxes(title_text="Энергия, МэВ")
spec_fig.update_yaxes(title_text="Плотность потока, нормированная на 1 и на ширину канала")

phi_fig.update_xaxes(title_text="Угол φ, град.")
phi_fig.update_yaxes(title_text="Плотность потока, нормированная на 1")

theta_fig.update_xaxes(title_text="Угол θ, град.")
theta_fig.update_yaxes(title_text="Плотность потока, нормированная на 1 и на единичный телесный угол")

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
                # html.Div(
                #     children=[
                #         html.Div(children="Quantity", className="menu-title"),
                #         dcc.Dropdown(
                #             id="quantity-filter",
                #             options=[
                #                 {"label": quantity, "value": quantity}
                #                 for quantity in QUANTITIES
                #             ],
                #             value="Spec",
                #             clearable=False,
                #             className="dropdown",
                #         ),
                #     ]
                # ),
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
                                multi=True,
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
                            value='1'
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
                        figure=spec_fig
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
                        id="phi-chart",
                        figure=phi_fig
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
                        figure=theta_fig
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
    Output('phi-chart', 'figure'),
    Output('theta-chart', 'figure'),
    Input('submit-plot', 'n_clicks'),
    State('tag-filter', 'value'),
    State('energy-filter', 'value'),
    State('num-filter', 'value'),
)
def plot_graph(n_clicks, tag, aenergies: list, anums):
    if n_clicks is None or n_clicks == 0:
        return spec_fig, phi_fig, theta_fig
    # clear all data 
    spec_fig.data = []
    phi_fig.data = []
    theta_fig.data = []

    energies = []
    if "All" in aenergies:
        energies = [i for i in ENERGY if i != "All"]
    else:
        energies = aenergies
    energies = [(float(i.split()[0]), i.split()[1]) for i in energies]
    nums = []
    if 'All' in anums:
        nums = [str(i) for i in range(1, NUMS[tag]+1)]
    else:
        nums = [i for i in anums]

    dets = dm.filterTag(detectors, tag)
    dets = dm.filterEnergies(dets, energies)
    dets = dm.filterNums(dets, nums)

    spec_dets = dm.filterQuantity(dets, 'Spec')
    # print(f'Фильтрую спек, получаю {len(spec_dets)} детекторов')
    phi_dets = dm.filterQuantity(dets, 'Phi')
    # print(f'Фильтрую фи, получаю {len(phi_dets)} детекторов')
    theta_dets = dm.filterQuantity(dets, 'Theta')
    # print(f'Фильтрую тета, получаю {len(theta_dets)} детекторов')
    for keyname, value in spec_dets.items():
        _, det = value
        plotNormWidthDetector(spec_fig, det, keyname)
    for keyname, value in phi_dets.items():
        _, det = value
        plotNormDetector(phi_fig, det, keyname)
    for keyname, value in theta_dets.items():
        _, det = value
        plotNormWidthTheta(theta_fig, det, keyname)

    return spec_fig, phi_fig, theta_fig

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