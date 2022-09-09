from dash import html

from .panel import panel
from .figures import figures

fig_content = html.Div(
    [
        panel,
        figures,
    ]
)