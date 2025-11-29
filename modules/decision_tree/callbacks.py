"""
Decision Tree Callbacks - Complete decision tree modeling with ICER calculations and database integration
"""
from dash import Input, Output, State, callback_context, html, ALL
import dash_bootstrap_components as dbc
from database.services import ProjectService, ScenarioService
import json


def calculate_expected_value(node, tree_data):
    """Recursively calculate expected value for a node"""
    if node['type'] == 'terminal':
        return node.get('cost', 0), node.get('effect', 0)
    
    children = [n for n in tree_data['nodes'] if n.get('parent_id') == node['id']]
    
    if node['type'] == 'decision':
        # For decision nodes, find the strategy with best expected value
        best_cost, best_effect = float('inf'), 0
        for child in children:
            cost, effect = calculate_expected_value(child, tree_data)
            if cost < best_cost or (cost == best_cost and effect > best_effect):
                best_cost, best_effect = cost, effect
        return best_cost, best_effect
    
    elif node['type'] == 'chance':
        # For chance nodes, calculate probability-weighted average
        total_cost, total_effect = 0, 0
        for child in children:
            prob = child.get('probability', 0)
            cost, effect = calculate_expected_value(child, tree_data)
            total_cost += prob * cost
            total_effect += prob * effect
        return total_cost, total_effect
    
    return 0, 0


def render_tree_node(node, level=0):
    """Render a tree node with visual styling"""
    icons = {
        'decision': 'fa-square',
        'chance': 'fa-circle',
        'terminal': 'fa-square-full'
    }
    
    colors = {
        'decision': 'primary',
        'chance': 'warning',
        'terminal': 'success'
    }
    
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className=f"fas {icons.get(node['type'], 'fa-circle')} me-2 text-{colors.get(node['type'], 'secondary')}"),
                    html.Strong(node.get('name', 'Unnamed')),
                    html.Small(f" (p={node.get('probability', 1.0):.2f})", className="text-muted ms-2") if node['type'] != 'decision' and node.get('probability') else None,
                ]),
                html.Small([
                    f"Cost: ${node.get('cost', 0):,.0f}" if node.get('cost') else "",
                    f" | Effect: {node.get('effect', 0):.2f} QALYs" if node.get('effect') else ""
                ], className="text-muted") if node['type'] == 'terminal' else None
            ], className="p-2"),
        ], className="mb-2", style={"marginLeft": f"{level * 30}px"})
    ])


def register_callbacks(app):
    """Register all decision tree callbacks"""
    
    @app.callback(
        Output('dt-project-select', 'options'),
        Input('url', 'pathname'),
        prevent_initial_call=False
    )
    def load_projects(pathname):
        """Load projects for decision tree"""
        if pathname != '/decision-tree':
            return []
        
        try:
            projects = ProjectService.list_projects(model_type='decision_tree')
            return [{'label': p['name'], 'value': p['id']} for p in projects]
        except:
            return []
    
    @app.callback(
        [Output('btn-new-dt-scenario', 'disabled'),
         Output('btn-add-node', 'disabled'),
         Output('btn-calculate-dt', 'disabled')],
        Input('dt-project-select', 'value')
    )
    def toggle_buttons(project_id):
        """Enable/disable buttons based on project selection"""
        if project_id:
            return False, False, False
        return True, True, True
    
    @app.callback(
        [Output('modal-new-dt-scenario', 'is_open'),
         Output('new-dt-scenario-name', 'value'),
         Output('new-dt-scenario-description', 'value')],
        [Input('btn-new-dt-scenario', 'n_clicks'),
         Input('btn-cancel-dt-scenario', 'n_clicks'),
         Input('btn-create-dt-scenario', 'n_clicks')],
        [State('modal-new-dt-scenario', 'is_open'),
         State('dt-project-select', 'value'),
         State('new-dt-scenario-name', 'value'),
         State('new-dt-scenario-description', 'value')],
        prevent_initial_call=True
    )
    def handle_scenario_modal(new_click, cancel_click, create_click,
                             is_open, project_id, name, description):
        """Handle scenario creation modal"""
        ctx = callback_context
        if not ctx.triggered:
            return is_open, "", ""
        
        trigger = ctx.triggered[0]['prop_id']
        
        if 'btn-new-dt-scenario' in trigger:
            return True, "", ""
        
        if 'btn-create-dt-scenario' in trigger and name and project_id:
            try:
                ScenarioService.create_scenario(
                    project_id=project_id,
                    name=name,
                    description=description or "",
                    parameters={}
                )
                return False, "", ""
            except Exception as e:
                print(f"Error creating scenario: {e}")
                return True, name, description
        
        return False, "", ""
    
    @app.callback(
        Output('dt-tree-data', 'data'),
        Input('btn-add-node', 'n_clicks'),
        State('dt-tree-data', 'data'),
        prevent_initial_call=True
    )
    def add_node(n_clicks, tree_data):
        """Add a new node to the tree"""
        if not tree_data:
            tree_data = {
                'nodes': [
                    {
                        'id': 0,
                        'type': 'decision',
                        'name': 'Treatment Decision',
                        'parent_id': None
                    }
                ]
            }
        else:
            new_id = max([n['id'] for n in tree_data['nodes']]) + 1
            tree_data['nodes'].append({
                'id': new_id,
                'type': 'terminal',
                'name': f'Outcome {new_id}',
                'parent_id': 0,
                'cost': 10000,
                'effect': 5.0,
                'probability': 0.5
            })
        
        return tree_data
    
    @app.callback(
        Output('decision-tree-canvas', 'children'),
        Input('dt-tree-data', 'data')
    )
    def render_tree(tree_data):
        """Render the decision tree"""
        if not tree_data or not tree_data.get('nodes'):
            return html.Div([
                html.I(className="fas fa-project-diagram fa-3x text-muted mb-3"),
                html.P("Click 'Add Node' to start building your tree", className="text-muted")
            ], className="text-center py-5")
        
        nodes = tree_data['nodes']
        return html.Div([
            render_tree_node(node, level=0 if node['id'] == 0 else 1)
            for node in nodes
        ])
    
    @app.callback(
        Output('dt-results', 'children'),
        [Input('btn-calculate-dt', 'n_clicks')],
        [State('dt-tree-data', 'data'),
         State('dt-discount-rate', 'value'),
         State('dt-time-horizon', 'value'),
         State('dt-wtp-threshold', 'value')],
        prevent_initial_call=True
    )
    def calculate_results(n_clicks, tree_data, discount_rate, time_horizon, wtp):
        """Calculate decision tree results and ICER"""
        if not tree_data or not tree_data.get('nodes'):
            return html.P("No tree data available", className="text-muted")
        
        try:
            root = next((n for n in tree_data['nodes'] if n.get('parent_id') is None), None)
            if not root:
                return html.P("Invalid tree structure", className="text-muted")
            
            total_cost, total_effect = calculate_expected_value(root, tree_data)
            
            discount_factor = (1 - (1 + discount_rate/100) ** -time_horizon) / (discount_rate/100) if discount_rate > 0 else time_horizon
            discounted_cost = total_cost * discount_factor
            discounted_effect = total_effect * discount_factor
            
            return html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Total Cost", className="text-muted mb-1"),
                                html.H4(f"${discounted_cost:,.0f}", className="mb-0")
                            ])
                        ])
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Total QALYs", className="text-muted mb-1"),
                                html.H4(f"{discounted_effect:.2f}", className="mb-0")
                            ])
                        ])
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Cost per QALY", className="mb-2"),
                        html.H4(f"${(discounted_cost/discounted_effect if discounted_effect > 0 else 0):,.0f}", className="mb-3"),
                        html.Hr(),
                        html.Div([
                            html.Strong("Cost-Effective: "),
                            dbc.Badge(
                                "Yes" if (discounted_cost/discounted_effect if discounted_effect > 0 else float('inf')) < wtp else "No",
                                color="success" if (discounted_cost/discounted_effect if discounted_effect > 0 else float('inf')) < wtp else "danger"
                            ),
                            html.Small(f" (WTP: ${wtp:,})", className="text-muted ms-2")
                        ])
                    ])
                ])
            ])
            
        except Exception as e:
            return dbc.Alert(f"Calculation error: {str(e)}", color="danger")

