
# package imports 
from dash import Dash, html

# local imports
from .components import title, fig_content

# DASH PART
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets
)
server = app.server

def serve_layout():
    return html.Div(
        [
            title,
            fig_content,
        ]
    )

app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(debug=True)
