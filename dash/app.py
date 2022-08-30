from dash import Dash, html, dcc, Input, Output
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
                    children=dcc.Graph(
                        id="spec-chart",
                        figure=fig
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)



# test data
# for right plot with 'vh' line_shape we need to put [0] to the begin of 'y' list
# y = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1] # len = 17
# y = [0] + y
# # bin i 0     1     2      3      4      5      6      7      8      9     10     11     12     13     14     15     16     17 
# x = [1.23, 4.56, 7.89, 10.11, 12.13, 14.15, 16.17, 18.19, 20.21, 22.23, 24.25, 26.27, 28.29, 30.31, 32.33, 34.35, 36.37, 38.39] # len = 18
# fig.add_trace(go.Scatter(
#     x = x,
#     y = y,
#     line_shape='vh',
#     name='test data'
# ))

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

if __name__ == "__main__":
    detectors = dm.prep_dets_for_filtering(dm.detectors)
    
    # Vert specs
    # dets = dm.filterQuantity(detectors, 'Spec')
    # dets = dm.filterTag(dets, 'Vert')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotMeansDetector(fig, det, keyname)
    # fig.update_layout(title_text='Спектры вертикальных детекторов для энергии 1 МэВ')

    # Vert specs norm
    # dets = dm.filterQuantity(detectors, 'Spec')
    # dets = dm.filterTag(dets, 'Vert')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormDetector(fig, det, keyname)
    # fig.update_layout(title_text='Нормированные спектры вертикальных детекторов для энергии 1 МэВ')

    # Vert specs norm 1 and width
    # dets = dm.filterQuantity(detectors, 'Spec')
    # dets = dm.filterTag(dets, 'Vert')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, keyname)
    # fig.update_layout(title_text='Нормированные на 1 и на ширину канала спектры вертикальных детекторов для энергии 1 МэВ')

    # Vert Phi norm 1
    # dets = dm.filterQuantity(detectors, 'Phi')
    # dets = dm.filterTag(dets, 'Vert')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormDetector(fig, det, keyname)
    # fig.update_layout(title_text='Нормированные на 1 и на ширину канала угловые (Phi) для вертикальных детекторов для энергии 1 МэВ')

    # Vert Theta norm 1
    # dets = dm.filterQuantity(detectors, 'Theta')
    # dets = dm.filterTag(dets, 'Vert')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormDetector(fig, det, keyname)
    # fig.update_layout(title_text='Нормированные на 1 и на ширину канала угловые (Theta) для вертикальных детекторов для энергии 1 МэВ')

    # Diag Spec 1 MeV
    # dets = dm.filterQuantity(detectors, 'Spec')
    # dets = dm.filterTag(dets, 'Diag')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotMeansDetector(fig, det, keyname)
    # fig.update_layout(title_text='Спектры для диагональных детекторов для энергии 1 МэВ')

    # Diag Spec 1 MeV
    # dets = dm.filterQuantity(detectors, 'Spec')
    # dets = dm.filterTag(dets, 'Diag')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'energy'}))
    # fig.update_layout(title_text='Нормированные на 1 и на ширину канала спектры для диагональных детекторов для энергии 1 МэВ')

    # Diag Phi 1 MeV
    # dets = dm.filterQuantity(detectors, 'Phi')
    # dets = dm.filterTag(dets, 'Diag')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'energy', 'Diag'}))
    # fig.update_layout(title_text='Нормированные на 1 и на ширину канала углы (Phi) для диагональных детекторов для энергии 1 МэВ')

    # Diag Theta 1 MeV
    # dets = dm.filterQuantity(detectors, 'Theta')
    # dets = dm.filterTag(dets, 'Diag')
    # dets = dm.filterEnergy(dets, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'energy', 'Diag'}))
    # fig.update_layout(title_text='Нормированные на 1 и на ширину канала углы (Theta) для диагональных детекторов для энергии 1 МэВ')

    # Diag Spec Different energies
    # detectors = dm.filterNum(detectors, '10')
    # detectors = dm.filterQuantity(detectors, 'Spec')
    # detectors = dm.filterTag(detectors, 'Diag')

    # dets = dm.filterEnergy(detectors, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'Diag'}))

    # dets = dm.filterEnergy(detectors, 100.0, 'keV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'Diag'}))

    # dets = dm.filterEnergy(detectors, 1.0, 'keV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'Diag'}))

    # dets = dm.filterEnergy(detectors, 1.0, 'eV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'Diag'}))

    # fig.update_layout(title_text='Спектры для диагональных детекторов для разных энергий')



    # Diag Phi Different energies
    # detectors = dm.filterNum(detectors, '1')
    # detectors = dm.filterQuantity(detectors, 'Theta')
    # detectors = dm.filterTag(detectors, 'XWall')

    # dets = dm.filterEnergy(detectors, 1.0, 'MeV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'XWall'}))

    # dets = dm.filterEnergy(detectors, 100.0, 'keV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'XWall'}))

    # dets = dm.filterEnergy(detectors, 1.0, 'keV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'XWall'}))

    # dets = dm.filterEnergy(detectors, 1.0, 'eV')
    # for keyname, value in dets.items():
    #     detset, det = value
    #     plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'XWall'}))

    # fig.update_layout(title_text='Угловые распределения (Theta) в XWall детекторе для разных энергий')
    # fig.update_layout(title_text='Спектры для вертикальных детекторов для разных энергий')

# XWall 
    # detectors = dm.filterNum(detectors, '1')
    detectors = dm.filterQuantity(detectors, 'Spec')
    detectors = dm.filterTag(detectors, 'XWall')

    dets = dm.filterEnergy(detectors, 1.0, 'MeV')
    for keyname, value in dets.items():
        detset, det = value
        plotNormWidthDetector(fig, det, det.detProps.getKeyname({'quantity', 'XWall', 'energy'}))

    # fig.update_layout(title_text='Угловые распределения (Theta) в XWall детекторе для разных энергий')
    fig.update_layout(title_text='Спектры для детекторов вдоль стены 50м для разных энергий')


    app.run_server(debug=True)