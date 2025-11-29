"""
Projects Layout - Project management page
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    # Header with action button
    dbc.Row([
        dbc.Col([
            dbc.Button([
                html.I(className="fas fa-plus me-2"),
                "New Project"
            ], id="btn-new-project", color="danger", className="float-end")
        ], width=12)
    ], className="mb-4"),
    
    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Input(
                id="project-search",
                placeholder="Search projects...",
                type="text",
                className="mb-3"
            )
        ], width=8),
        dbc.Col([
            dcc.Dropdown(
                id="project-type-filter",
                options=[
                    {'label': 'All Types', 'value': 'all'},
                    {'label': 'Decision Tree', 'value': 'decision_tree'},
                    {'label': 'Markov Model', 'value': 'markov'},
                    {'label': 'PSM', 'value': 'psm'},
                ],
                value='all',
                clearable=False,
                className="mb-3"
            )
        ], width=4),
    ]),
    
    # Projects list
    dbc.Row([
        dbc.Col([
            html.Div(id="projects-list", children=[
                dbc.Card([
                    dbc.CardBody([
                        html.P("No projects yet. Click 'New Project' to get started!", 
                               className="text-center text-muted py-5 mb-0")
                    ])
                ])
            ])
        ])
    ]),
    
    # New Project Modal
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Create New Project")),
        dbc.ModalBody([
            dbc.Label("Project Name"),
            dbc.Input(id="new-project-name", placeholder="Enter project name", className="mb-3"),
            
            dbc.Label("Description"),
            dbc.Textarea(id="new-project-description", placeholder="Project description", className="mb-3"),
            
            dbc.Label("Model Type"),
            dcc.Dropdown(
                id="new-project-type",
                options=[
                    {'label': 'Decision Tree', 'value': 'decision_tree'},
                    {'label': 'Markov Model', 'value': 'markov'},
                    {'label': 'Partitioned Survival Model (PSM)', 'value': 'psm'},
                ],
                placeholder="Select model type"
            )
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="btn-cancel-project", color="secondary", className="me-2"),
            dbc.Button("Create Project", id="btn-create-project", color="danger")
        ])
    ], id="modal-new-project", size="lg", is_open=False),
    
], fluid=True)
