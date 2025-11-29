"""
Projects Callbacks - Handle project-related interactions
"""
from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import html

# Import database functions
from data.database import get_all_projects, create_project, delete_project

def register_callbacks(app):
    """Register all project-related callbacks"""
    
    @app.callback(
        Output("modal-new-project", "is_open"),
        [Input("btn-new-project", "n_clicks"),
         Input("btn-cancel-project", "n_clicks"),
         Input("btn-create-project", "n_clicks")],
        [State("modal-new-project", "is_open")]
    )
    def toggle_project_modal(n1, n2, n3, is_open):
        """Toggle new project modal"""
        if n1 or n2 or n3:
            return not is_open
        return is_open
    
    @app.callback(
        Output("projects-list", "children"),
        [Input("project-search", "value"),
         Input("project-type-filter", "value"),
         Input("project-status-filter", "value"),
         Input("btn-create-project", "n_clicks")],
        [State("new-project-name", "value"),
         State("new-project-description", "value"),
         State("new-project-type", "value")]
    )
    def update_projects_list(search, type_filter, status_filter, n_clicks, name, description, project_type):
        """Update projects list based on filters"""
        ctx = callback_context
        
        # If creating a new project
        if ctx.triggered and ctx.triggered[0]['prop_id'] == 'btn-create-project.n_clicks':
            if name and project_type:
                create_project(name, description or "", project_type)
        
        # Get all projects
        projects = get_all_projects()
        
        # Apply filters
        if type_filter != 'all':
            projects = [p for p in projects if p['model_type'] == type_filter]
        if status_filter != 'all':
            projects = [p for p in projects if p['status'] == status_filter]
        if search:
            projects = [p for p in projects if search.lower() in p['name'].lower()]
        
        # Create project cards
        if not projects:
            return dbc.Card([
                dbc.CardBody([
                    html.P("No projects found", className="text-center text-muted py-5 mb-0")
                ])
            ])
        
        cards = []
        for project in projects:
            card = dbc.Card([
                dbc.CardBody([
                    html.H5(project['name'], className="card-title"),
                    html.P(project['description'] or "No description", className="card-text text-muted"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge(project['model_type'].replace('_', ' ').title(), color="danger", className="me-2"),
                            dbc.Badge(project['status'].capitalize(), color="secondary")
                        ], width=8),
                        dbc.Col([
                            dbc.ButtonGroup([
                                dbc.Button(html.I(className="fas fa-edit"), size="sm", color="outline-danger"),
                                dbc.Button(html.I(className="fas fa-trash"), size="sm", color="outline-danger"),
                            ], className="float-end")
                        ], width=4)
                    ])
                ])
            ], className="mb-3 shadow-sm")
            cards.append(card)
        
        return cards
