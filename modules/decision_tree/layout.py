"""Decision Tree Layout - Decision tree modeling page"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Decision Tree", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Tree Builder", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="decision-tree-builder", children=[
                        html.P("Decision tree builder will be implemented here", className="text-muted")
                    ])
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Parameters", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="decision-tree-parameters")
                ])
            ])
        ], width=4),
    ])
], fluid=True)
