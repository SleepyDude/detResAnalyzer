from dash import html, Output, Input, callback
from pandas import DataFrame

from typing import List

# global var, tie with the file, bad practice, need to be fixed
table_data = {}

def generate_tr(row: List[str]):
    tds = []
    for item in list(row):
        if type(item) == str and item.startswith('rgb(') or type(item) == tuple and len(item) == 3:
            rgb = ""
            if type(item) == tuple:
                rgb = f"rgb({item[0]*255}, {item[1]*255}, {item[2]*255})"
            else:
                rgb = item
            tds.append(html.Td("",
                style={'backgroundColor': rgb},
            ))
        else:
            tds.append(html.Td(item))
    tr = html.Tr(
        tds
    )
    return tr

def generate_table(df = None):
    if df is None:
        return html.Table(
            "",
            id="trace-table",
            className="table table-striped table-bordered table-hover",
        )

    thead = html.Thead(
        html.Tr(
            [
                html.Th(item) 
                for item in list(df)
            ]
        )
    )

    tbody = html.Tbody(
        [
            generate_tr(row)
            for _, row in df.iterrows()
        ]
    )

    return thead, tbody

# initial table (empty table)
trace_table = html.Table(
    "",
    id="trace-table",
    className="table table-striped table-bordered table-hover",
)

@callback(
    Output('trace-table', 'children'),
    Input('theta-chart', 'figure'),
)
def create_table(fig):
    # print(table_data)
    thead, tbody = generate_table(DataFrame(table_data))
    return [thead, tbody]