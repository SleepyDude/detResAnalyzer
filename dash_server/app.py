
# package imports 
from dash import Dash, html
import dash_bootstrap_components as dbc

# local imports
from .components import title, fig_content, fig_panel

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[
        {'name': 'viewport',
         'content': 'width=device-width initial-scale=1.0'
        }
    ]
)
server = app.server

def serve_layout():
    return dbc.Container(
        [
            dbc.Row([
                title
            ]),
            dbc.Container(
                [
                    fig_panel,
                    fig_content,
                ]
            ),
        ],
        fluid=True,
        className="bg-light"
    )
    # return html.Div(
    #     [
    #         title,
    #         fig_content,
    #     ]
    # )

app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(debug=True)
