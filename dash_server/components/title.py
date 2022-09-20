
from dash import html
import dash_bootstrap_components as dbc

title = dbc.Col(
    children=[
        html.H2(
            children="Аналитика Детекторов",
            className="mt-3",
        ),
        html.P(
            children="Анализ зависимости спектра и углового распределения."
            " Источник расположен в углу комнаты на высоте 1.5 м. и на расстоянии 0.5 м. от стен",
            className="title-bottom col-lg-10 offset-1",
        ),
    ],
    className="text-center bg-primary text-white",
)