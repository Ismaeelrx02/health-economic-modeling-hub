"""PSA Layout - Probabilistic Sensitivity Analysis page"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Probabilistic Analysis", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Cost-Effectiveness Acceptability Curve (CEAC)", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="psa-ceac-chart")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Scatter Plot", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="psa-scatter-plot")
                ])
            ])
        ], width=6),
    ])
], fluid=True)
