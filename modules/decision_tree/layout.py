"""Decision Tree Layout - Complete decision tree modeling with calculations"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    # Project selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="dt-project-select",
                                placeholder="Select a project...",
                                className="mb-0"
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-plus me-2"),
                                "New Scenario"
                            ], id="btn-new-dt-scenario", color="danger", disabled=True)
                        ], width=4, className="d-flex justify-content-end")
                    ])
                ])
            ])
        ])
    ], className="mb-3"),
    
    # Main content
    dbc.Row([
        # Tree structure
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Tree Structure", className="mb-0 d-inline"),
                    dbc.Button(
                        html.I(className="fas fa-plus"),
                        id="btn-add-node",
                        size="sm",
                        color="danger",
                        outline=True,
                        className="float-end",
                        disabled=True
                    )
                ]),
                dbc.CardBody([
                    html.Div(id="decision-tree-canvas", children=[
                        html.Div([
                            html.I(className="fas fa-project-diagram fa-3x text-muted mb-3"),
                            html.P("Select a project to start building your decision tree", className="text-muted mb-0")
                        ], className="text-center py-5")
                    ])
                ])
            ], className="mb-3"),
            
            # Results
            dbc.Card([
                dbc.CardHeader(html.H5("Results", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="dt-results")
                ])
            ])
        ], width=8),
        
        # Parameters panel
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Parameters", className="mb-0")),
                dbc.CardBody([
                    html.Div([
                        # Discount rate
                        html.Label("Discount Rate (%)", className="form-label"),
                        dbc.Input(
                            id="dt-discount-rate",
                            type="number",
                            value=3.0,
                            min=0,
                            max=10,
                            step=0.1,
                            className="mb-3"
                        ),
                        
                        # Time horizon
                        html.Label("Time Horizon (years)", className="form-label"),
                        dbc.Input(
                            id="dt-time-horizon",
                            type="number",
                            value=10,
                            min=1,
                            max=50,
                            step=1,
                            className="mb-3"
                        ),
                        
                        # WTP threshold
                        html.Label("WTP Threshold ($)", className="form-label"),
                        dbc.Input(
                            id="dt-wtp-threshold",
                            type="number",
                            value=50000,
                            min=0,
                            step=1000,
                            className="mb-3"
                        ),
                        
                        html.Hr(),
                        
                        # Calculate button
                        dbc.Button([
                            html.I(className="fas fa-calculator me-2"),
                            "Calculate"
                        ], id="btn-calculate-dt", color="danger", className="w-100", disabled=True)
                    ])
                ])
            ], className="mb-3"),
            
            # Node editor (appears when node selected)
            html.Div(id="dt-node-editor")
        ], width=4)
    ]),
    
    # Modals
    dbc.Modal([
        dbc.ModalHeader("New Scenario"),
        dbc.ModalBody([
            html.Label("Scenario Name", className="form-label"),
            dbc.Input(id="new-dt-scenario-name", placeholder="e.g., Base Case"),
            html.Label("Description", className="form-label mt-3"),
            dbc.Textarea(id="new-dt-scenario-description", placeholder="Optional description...")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="btn-cancel-dt-scenario", color="secondary"),
            dbc.Button("Create", id="btn-create-dt-scenario", color="danger")
        ])
    ], id="modal-new-dt-scenario"),
    
    # Store for tree data
    dcc.Store(id="dt-tree-data")
], fluid=True)
