"""
Projects Module - Complete Callbacks with Database Integration
Full CRUD operations for project management
"""
from dash import Input, Output, State, ALL, callback_context, html
import dash_bootstrap_components as dbc
from database.services import ProjectService
from datetime import datetime


def create_project_card(project):
    """Create a project card from project data"""
    model_type_colors = {
        'decision_tree': 'info',
        'markov': 'success',
        'psm': 'warning'
    }
    
    model_type_labels = {
        'decision_tree': 'Decision Tree',
        'markov': 'Markov Model',
        'psm': 'PSM'
    }
    
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.H5(project['name'], className="mb-0 d-inline"),
                    dbc.Badge(
                        model_type_labels.get(project['model_type'], project['model_type']),
                        color=model_type_colors.get(project['model_type'], 'secondary'),
                        className="float-end"
                    )
                ])
            ]),
            dbc.CardBody([
                html.P(
                    project.get('description', 'No description')[:100] + ('...' if len(project.get('description', '')) > 100 else ''),
                    className="text-muted mb-2"
                ),
                html.Div([
                    html.Small([
                        html.I(className="fas fa-calendar me-1"),
                        f"Created: {datetime.fromisoformat(project['created_at']).strftime('%b %d, %Y')}"
                    ], className="text-muted me-3"),
                    html.Small([
                        html.I(className="fas fa-layer-group me-1"),
                        f"{project.get('scenarios_count', 0)} scenarios"
                    ], className="text-muted")
                ])
            ]),
            dbc.CardFooter([
                dbc.ButtonGroup([
                    dbc.Button(
                        [html.I(className="fas fa-folder-open me-1"), "Open"],
                        id={'type': 'btn-open-project', 'index': project['id']},
                        size="sm",
                        color="danger"
                    ),
                    dbc.Button(
                        html.I(className="fas fa-edit"),
                        id={'type': 'btn-edit-project', 'index': project['id']},
                        size="sm",
                        color="secondary",
                        outline=True
                    ),
                    dbc.Button(
                        html.I(className="fas fa-trash"),
                        id={'type': 'btn-delete-project', 'index': project['id']},
                        size="sm",
                        color="danger",
                        outline=True
                    )
                ], className="w-100")
            ])
        ], className="mb-3 h-100")
    ], width=12, lg=4, className="mb-3")


def register_callbacks(app):
    """Register all project-related callbacks"""
    
    @app.callback(
        Output('projects-list', 'children'),
        [Input('btn-refresh-projects', 'n_clicks') if hasattr(app, 'btn-refresh-projects') else Input('url', 'pathname'),
         Input('project-type-filter', 'value'),
         Input('project-search', 'value')],
        prevent_initial_call=False
    )
    def load_projects(refresh, filter_type, search):
        """Load and display projects from database"""
        try:
            # Get projects from database
            if filter_type and filter_type != 'all':
                projects = ProjectService.list_projects(model_type=filter_type)
            else:
                projects = ProjectService.list_projects()
            
            # Apply search filter
            if search:
                search_lower = search.lower()
                projects = [p for p in projects if search_lower in p['name'].lower() or 
                           search_lower in p.get('description', '').lower()]
            
            if not projects:
                return dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-folder-open fa-3x text-muted mb-3"),
                            html.H5("No projects found", className="text-muted"),
                            html.P("Create your first project to get started", className="text-muted")
                        ], className="text-center py-5")
                    ])
                ])
            
            # Create project cards in a row
            return dbc.Row([create_project_card(project) for project in projects])
            
        except Exception as e:
            return dbc.Alert(f"Error loading projects: {str(e)}", color="danger")
    
    @app.callback(
        [Output('modal-new-project', 'is_open'),
         Output('new-project-name', 'value'),
         Output('new-project-description', 'value'),
         Output('new-project-type', 'value')],
        [Input('btn-new-project', 'n_clicks'),
         Input('btn-cancel-project', 'n_clicks'),
         Input('btn-create-project', 'n_clicks')],
        [State('modal-new-project', 'is_open'),
         State('new-project-name', 'value'),
         State('new-project-type', 'value'),
         State('new-project-description', 'value')],
        prevent_initial_call=True
    )
    def handle_project_modal(new_clicks, cancel_clicks, create_clicks,
                            is_open, name, model_type, description):
        """Handle project modal and creation"""
        ctx = callback_context
        if not ctx.triggered:
            return is_open, "", "", None
        
        trigger_id = ctx.triggered[0]['prop_id']
        
        # New project button clicked
        if 'btn-new-project' in trigger_id:
            return True, "", "", None
        
        # Cancel button clicked
        if 'btn-cancel-project' in trigger_id:
            return False, "", "", None
        
        # Create button clicked
        if 'btn-create-project' in trigger_id:
            if not name or not model_type:
                return True, name, description, model_type
            
            try:
                # Create new project in database
                ProjectService.create_project(
                    name=name,
                    model_type=model_type,
                    description=description or ""
                )
                
                return False, "", "", None
            except Exception as e:
                print(f"Error creating project: {e}")
                return True, name, description, model_type
        
        return is_open, "", "", None
