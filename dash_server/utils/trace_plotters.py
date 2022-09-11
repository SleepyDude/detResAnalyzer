# modules
import plotly.graph_objects as go
import distinctipy

# local imports
from ...anadet.detector import Detector

colors = distinctipy.get_colors(40)
def gen_col() -> tuple:
    gen_col.i += 1
    if gen_col.i >= len(colors):
        gen_col.i = 0
    return colors[gen_col.i]
gen_col.i = 13

def plotMeansDetector(fig: go.Figure, det: Detector, name: str, col = None):
    if col is None:
        col = gen_col()
    x, y, _, _ = det.get_means_hl()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({col[0]},{col[1]},{col[2]})',
        name=name,
        line_shape='vh',
    ))

def plotNormDetector(fig: go.Figure, det: Detector, name: str, col = None):
    if col is None:
        col = gen_col()
    x, y, = det.get_norm_hl()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({col[0]},{col[1]},{col[2]})',
        name=name,
        line_shape='vh',
    ))

def plotNormWidthDetector(fig: go.Figure, det: Detector, name: str, col = None):
    if col is None:
        col = gen_col()
    x, y, = det.get_norm_width_hl()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({col[0]},{col[1]},{col[2]})',
        name=name,
        line_shape='vh',
    ))

def plotNormWidthTheta(fig: go.Figure, det: Detector, name: str, col = None):
    if col is None:
        col = gen_col()
    x, y, = det.get_norm_width_theta_hl()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({col[0]},{col[1]},{col[2]})',
        name=name,
        line_shape='vh',
    ))

def plotNormWidthPhi(fig: go.Figure, det: Detector, name: str, col = None):
    if col is None:
        col = gen_col()
    x, y, = det.get_norm_width_phi_hl()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        line_color=f'rgb({col[0]},{col[1]},{col[2]})',
        name=name,
        line_shape='vh',
    ))



