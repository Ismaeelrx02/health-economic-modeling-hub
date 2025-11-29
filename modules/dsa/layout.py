"""DSA Layout - Deterministic Sensitivity Analysis page"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Sensitivity Analysis", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Tornado Diagram", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="dsa-tornado-diagram")
                ])
            ])
        ])
    ])
], fluid=True)
