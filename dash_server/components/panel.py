
from dash import html, dcc, callback, Input, Output

QUANTITIES = ['Spec', 'Phi', 'Theta']
TAGS = ['Vert', 'Diag', 'XWall', 'YWall']
ENERGY = ['1 MeV', '100 keV', '1 keV', '1 eV', 'All']
NUMS = {
    'Vert': 8,
    'Diag': 10,
    'XWall': 10,
    'YWall': 10
}

up_menu = html.Div(
    children=[
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
)

down_menu = html.Div(
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
)

panel = html.Div(
    [
        up_menu,
        down_menu,
    ]
)

@callback(
    Output('num-filter', 'options'),
    Input('tag-filter', 'value')
)
def update_num_filter(tag):
    options = [str(i) for i in range(1,NUMS[tag]+1)]
    options.append('All')
    return options