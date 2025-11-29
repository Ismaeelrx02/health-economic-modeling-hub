"""Markov Model Layout - Markov cohort simulation page"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Markov Cohort Model", className="mb-4"),
    html.P("Build and simulate Markov cohort models", className="text-muted mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("State Diagram", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="markov-state-diagram")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Transition Matrix", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="markov-transition-matrix")
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Results", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="markov-results")
                ])
            ])
        ])
    ])
], fluid=True)
