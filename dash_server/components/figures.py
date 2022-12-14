from dash import html, dcc, Output, Input, State, callback
import plotly.graph_objects as go

from ...anadet.detector import Detector

from ..load_results import detectors, dm
from .panel import ENERGY, NUMS

spec_fig = go.Figure()
phi_fig = go.Figure()
theta_fig = go.Figure()

spec_fig.update_xaxes(type="log")
spec_fig.update_yaxes(type="log")

phi_fig.update_yaxes(type="log")
theta_fig.update_yaxes(type="log")


def update_layout(fig, xaxis_title, yaxis_title):
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        font=dict(
            size=18,
        ),
        legend=dict(
            font=dict(
                size=11,
            ),
        ),
        hovermode='x unified',
        height=800,
    )
update_layout(spec_fig, "Энергия, МэВ", "Плотность потока, норм. на 1 и на ширину канала")
update_layout(phi_fig, "Угол φ, град.", "Плотность потока, норм. на 1 и на ед. тел. угол")
update_layout(theta_fig, "Угол θ, град.", "Плотность потока, норм. на 1 и на ед. тел. угол")

spec_fig_layout = html.Div(
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
)

phi_fig_layout = html.Div(
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
)

theta_fig_layout = html.Div(
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
)

figures = html.Div(
    [
        spec_fig_layout,
        phi_fig_layout,
        theta_fig_layout,
    ]
)

import distinctipy

colors = distinctipy.get_colors(40)
def gen_col():
    gen_col.i += 1
    if gen_col.i >= len(colors):
        gen_col.i = 0
    return colors[gen_col.i]
gen_col.i = 13

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

def plotNormWidthPhi(fig: go.Figure, det: Detector, name: str):
    x, y, = det.get_norm_width_phi_hl()
    color = gen_col()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({color[0]},{color[1]},{color[2]})',
        name=name,
        line_shape='vh',
    ))





@callback(
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
    # clear all figures data
    spec_fig.data = []
    phi_fig.data = []
    theta_fig.data = []
    # end clear
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
    
    
    # Creating titles for figures
    params_name = tag + ", "
    if len(energies) > 1:
        params_name += " различные энергии, "
    else:
        params_name += f" энергия {energies[0][0]} {energies[0][1]}, "
    if len(nums) == 1:
        params_name += f"{nums[0]}-й детектор"
    else:
        params_name += "различные детекторы"
    spec_name = "Спектр " + params_name
    phi_name = "Угловое φ " + params_name
    theta_name = "Угловое θ " + params_name
    spec_fig.update_layout(title=spec_name)
    phi_fig.update_layout(title=phi_name)
    theta_fig.update_layout(title=theta_name)

    dets = dm.filterTag(detectors, tag)
    dets = dm.filterEnergies(dets, energies)
    dets = dm.filterNums(dets, nums)

    spec_dets = dm.filterQuantity(dets, 'Spec')
    phi_dets = dm.filterQuantity(dets, 'Phi')
    theta_dets = dm.filterQuantity(dets, 'Theta')
    for keyname, value in spec_dets.items():
        _, det = value
        plotNormWidthDetector(spec_fig, det, keyname)
    for keyname, value in phi_dets.items():
        _, det = value
        plotNormWidthPhi(phi_fig, det, keyname)
    for keyname, value in theta_dets.items():
        _, det = value
        plotNormWidthTheta(theta_fig, det, keyname)

    return spec_fig, phi_fig, theta_fig