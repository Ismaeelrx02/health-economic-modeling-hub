"""Base Case Layout - Base case analysis and comparison"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("ICER Analysis", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="base-case-icer-chart")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Cost-Effectiveness Plane", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="base-case-ce-plane")
                ])
            ])
        ], width=6),
    ])
], fluid=True)
