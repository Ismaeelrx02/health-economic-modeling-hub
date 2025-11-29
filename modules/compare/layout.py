"""Compare Layout - Model comparison page"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Compare Strategies", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("ICER Analysis", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="compare-icer-chart")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Cost-Effectiveness Plane", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id="compare-ce-plane")
                ])
            ])
        ], width=6),
    ])
], fluid=True)
