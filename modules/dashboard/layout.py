"""
Dashboard Layout - Main landing page
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Dashboard layout
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Health Economic Modeling Hub", className="mb-2"),
            html.P("Professional cost-effectiveness analysis platform", className="text-muted")
        ])
    ], className="mb-4"),
    
    # Statistics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("0", id="stat-total-projects", className="mb-2"),
                    html.P("Total Projects", className="text-muted mb-0")
                ])
            ], className="shadow-sm")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("0", id="stat-decision-trees", className="mb-2"),
                    html.P("Decision Trees", className="text-muted mb-0")
                ])
            ], className="shadow-sm")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("0", id="stat-markov-models", className="mb-2"),
                    html.P("Markov Models", className="text-muted mb-0")
                ])
            ], className="shadow-sm")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("0", id="stat-psm-models", className="mb-2"),
                    html.P("PSM Models", className="text-muted mb-0")
                ])
            ], className="shadow-sm")
        ], width=3),
    ], className="mb-4"),
    
    # Quick Actions
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Quick Actions", className="mb-0")),
                dbc.CardBody([
                    dbc.Button([
                        html.I(className="fas fa-plus me-2"),
                        "New Project"
                    ], color="danger", className="w-100 mb-2", href="/projects"),
                    
                    dbc.Button([
                        html.I(className="fas fa-sitemap me-2"),
                        "Build Decision Tree"
                    ], color="outline-danger", className="w-100 mb-2", href="/decision-tree"),
                    
                    dbc.Button([
                        html.I(className="fas fa-project-diagram me-2"),
                        "Create Markov Model"
                    ], color="outline-danger", className="w-100 mb-2", href="/markov"),
                    
                    dbc.Button([
                        html.I(className="fas fa-chart-line me-2"),
                        "Build PSM Model"
                    ], color="outline-danger", className="w-100", href="/psm"),
                ])
            ], className="shadow-sm")
        ], width=4),
        
        # Recent Activity
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Recent Activity", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="recent-activity", children=[
                        html.P("No recent activity", className="text-muted text-center py-4")
                    ])
                ])
            ], className="shadow-sm")
        ], width=8),
    ]),
    
    # Auto-refresh data
    dcc.Interval(id='dashboard-interval', interval=5000, n_intervals=0)
    
], fluid=True)
