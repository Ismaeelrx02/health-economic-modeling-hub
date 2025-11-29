"""PSM Layout - Partitioned Survival Model page"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Survival Curves", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="psm-survival-curves")
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Parameters", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="psm-parameters")
                ])
            ])
        ], width=4),
    ])
], fluid=True)
