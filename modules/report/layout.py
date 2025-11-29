"""Report Layout - Generate and view comprehensive reports"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Report Options", className="mb-0 d-inline"),
                    dbc.Button([
                        html.I(className="fas fa-file-pdf me-2"),
                        "Export PDF"
                    ], color="danger", size="sm", className="float-end")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Checklist(
                                options=[
                                    {"label": "Executive Summary", "value": "summary"},
                                    {"label": "Model Structure", "value": "structure"},
                                    {"label": "Base Case Results", "value": "base_case"},
                                    {"label": "Sensitivity Analysis", "value": "sensitivity"},
                                    {"label": "Probabilistic Analysis", "value": "probabilistic"},
                                    {"label": "Appendices", "value": "appendices"}
                                ],
                                value=["summary", "base_case"],
                                id="report-sections"
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Report Format", className="form-label"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "PDF", "value": "pdf"},
                                    {"label": "Word", "value": "docx"},
                                    {"label": "HTML", "value": "html"}
                                ],
                                value="pdf",
                                id="report-format"
                            )
                        ], width=6)
                    ])
                ])
            ])
        ])
    ], className="mb-3"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Report Preview", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="report-preview", children=[
                        html.P("Configure options above and generate report", className="text-muted text-center py-5")
                    ])
                ])
            ])
        ])
    ])
], fluid=True)
