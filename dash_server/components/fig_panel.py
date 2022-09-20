
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

QUANTITIES = ['Spec', 'Phi', 'Theta']
TAGS = ['Vert', 'Diag', 'XWall', 'YWall']
ENERGY = ['1 MeV', '100 keV', '1 keV', '1 eV', 'All']
NUMS = {
    'Vert': 8,
    'Diag': 10,
    'XWall': 10,
    'YWall': 10
}

up_panel_row = dbc.Row(
    children=[
        dbc.Col(
            children=[
                html.Div(children="Type"),
                dcc.Dropdown(
                    id="tag-filter",
                    options=[
                        {"label": tag, "value": tag}
                        for tag in TAGS
                    ],
                    value="Vert",
                    clearable=False,
                    searchable=False,
                ),
            ],
            className='col-4',
        ),
        dbc.Col(
            children=[
                html.Div(
                    children="Energy",
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
                    multi=True,
                ),
            ],
            className='col-8',
        ),
    ],
    className="form-group",
)

down_panel_row = dbc.Row(
    children=[
        dbc.Col(
            children=[
                html.Div(
                    children="Num",
                ),
                dcc.Dropdown(
                    id="num-filter",
                    options=[],
                    multi=True,
                    value='1'
                ),
            ],
            className='col-8',
        ),
        dbc.Col(
            children=[
                html.Div(
                    children="...",
                ),
                html.Button(
                    'Plot', 
                    id='submit-plot',
                    n_clicks=0,
                    className="Select-control btn-plot"
                ),
            ],
            className='col-4',
        ),
    ],
    className="form-group mb-2",
)

fig_panel = dbc.Row(
    dbc.Col(
        [
            up_panel_row,
            down_panel_row,
        ],
        className="col-lg-10 fig_panel bg-white rounded text-green-pl"
    ),
    className="d-flex justify-content-center mb-3"
    # className='shadow-sm bg-light rounded mt-2 mb-2 w-75 mx-auto'
)

@callback(
    Output('num-filter', 'options'),
    Input('tag-filter', 'value')
)
def update_num_filter(tag):
    options = [str(i) for i in range(1,NUMS[tag]+1)]
    options.append('All')
    return options