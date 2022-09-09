
from dash import html

title = html.Div(
    children=[
        html.H1(
            children="Аналитика Детекторов", className="header-title"
        ),
        html.P(
            children="Анализ зависимости спектра и углового распределения."
            " Источник расположен в углу комнаты на высоте 1.5 м. и на расстоянии 0.5 м. от стен",
            className="header-description",
        ),
    ],
    className="header",
)