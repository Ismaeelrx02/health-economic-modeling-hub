"""
Health Economic Modeling Hub - Dash Application
Module-based architecture with integrated layouts and callbacks
Red, White, and Black color scheme with collapsible sidebar
"""
import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Import configuration
from config.settings import THEME, APP_TITLE, PORT, HOST

# Import modules (each has layout + callbacks together)
from modules.dashboard import layout as dashboard_layout
from modules.projects import layout as projects_layout, register_callbacks as projects_callbacks
from modules.decision_tree import layout as decision_tree_layout, register_callbacks as decision_tree_callbacks
from modules.markov import layout as markov_layout, register_callbacks as markov_callbacks
from modules.psm import layout as psm_layout, register_callbacks as psm_callbacks
from modules.compare import layout as compare_layout, register_callbacks as compare_callbacks
from modules.dsa import layout as dsa_layout, register_callbacks as dsa_callbacks
from modules.psa import layout as psa_layout, register_callbacks as psa_callbacks

# Initialize Dash app with Bootstrap theme + custom assets
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    external_scripts=[],
    suppress_callback_exceptions=True,
    title=APP_TITLE,
    use_pages=False,  # Manual page routing for full control
    assets_folder='assets'  # Dash automatically loads custom.css and app.js from assets/
)

# App layout with collapsible sidebar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='ai-mode-store', data='ai-assisted'),  # Store AI mode globally
    dcc.Store(id='sidebar-state', data={'collapsed': False}),  # Store sidebar state
    
    # Header Bar (Red background)
    html.Div([
        html.Div([
            # Hamburger menu button
            html.Button(
                html.I(className="fas fa-bars"),
                id='sidebar-toggle',
                className='sidebar-toggle-btn',
                n_clicks=0
            ),
            # App title
            html.Span([
                html.Strong("Health Economic Modeling Hub", className='app-title')
            ]),
            # Right side controls
            html.Div([
                dcc.Dropdown(
                    id='ai-mode-dropdown',
                    options=[
                        {'label': 'AI-Assisted', 'value': 'ai-assisted'},
                        {'label': 'AI-Augmented', 'value': 'ai-augmented'},
                        {'label': 'AI-Automated', 'value': 'ai-automated'}
                    ],
                    value='ai-assisted',
                    clearable=False,
                    searchable=False,
                    className='ai-mode-dropdown'
                ),
                html.Span(id='ai-mode-indicator', className="ai-mode-badge"),
                html.Button(
                    html.I(className="fas fa-robot"),
                    id='ai-assistant-btn',
                    className='ai-assistant-btn',
                    title='AI Assistant'
                )
            ], className='header-right')
        ], className='header-content')
    ], className='app-header'),
    
    # Main container with sidebar and content
    html.Div([
        # Collapsible Sidebar (Red background)
        html.Div([
            html.Div([
                # Home
                dbc.NavLink([
                    html.I(className="fas fa-home"),
                    html.Span("Home", className='nav-text')
                ], href="/", id="nav-dashboard", className='nav-item'),
                
                # Repository (Projects)
                dbc.NavLink([
                    html.I(className="fas fa-archive"),
                    html.Span("Repository", className='nav-text')
                ], href="/projects", id="nav-projects", className='nav-item'),
                
                # Protocol
                dbc.NavLink([
                    html.I(className="fas fa-file-alt"),
                    html.Span("Protocol", className='nav-text')
                ], href="/protocol", id="nav-protocol", className='nav-item'),
                
                # Literature Search
                dbc.NavLink([
                    html.I(className="fas fa-search"),
                    html.Span("Literature Search", className='nav-text')
                ], href="/literature", id="nav-literature", className='nav-item'),
                
                # Article Screening
                dbc.NavLink([
                    html.I(className="fas fa-filter"),
                    html.Span("Article Screening", className='nav-text')
                ], href="/decision-tree", id="nav-screening", className='nav-item'),
                
                # Study Quality
                dbc.NavLink([
                    html.I(className="fas fa-check-circle"),
                    html.Span("Study Quality", className='nav-text')
                ], href="/markov", id="nav-quality", className='nav-item'),
                
                # Data Extraction
                dbc.NavLink([
                    html.I(className="fas fa-database"),
                    html.Span("Data Extraction", className='nav-text')
                ], href="/psm", id="nav-extraction", className='nav-item'),
                
                # Evidence Synthesis
                dbc.NavLink([
                    html.I(className="fas fa-chart-bar"),
                    html.Span("Evidence Synthesis", className='nav-text')
                ], href="/compare", id="nav-synthesis", className='nav-item'),
                
                # Report
                dbc.NavLink([
                    html.I(className="fas fa-file-pdf"),
                    html.Span("Report", className='nav-text')
                ], href="/dsa", id="nav-report", className='nav-item'),
                
                # Settings & Team
                dbc.NavLink([
                    html.I(className="fas fa-cog"),
                    html.Span("Settings & Team", className='nav-text')
                ], href="/psa", id="nav-settings", className='nav-item'),
            ], className='sidebar-nav')
        ], id='sidebar', className='app-sidebar'),
        
        # Main content area
        html.Div([
            html.Div(id='page-content', className="p-4")
        ], id='main-content', className='app-content')
    ], className='app-container')
], className='app-wrapper')

# Callback for sidebar collapse/expand
@app.callback(
    Output('sidebar', 'className'),
    Output('main-content', 'className'),
    Output('sidebar-state', 'data'),
    Input('sidebar-toggle', 'n_clicks'),
    State('sidebar-state', 'data')
)
def toggle_sidebar(n_clicks, state):
    """Toggle sidebar collapsed/expanded state"""
    if n_clicks is None:
        return 'app-sidebar', 'app-content', state
    
    collapsed = not state.get('collapsed', False)
    
    if collapsed:
        return 'app-sidebar collapsed', 'app-content expanded', {'collapsed': True}
    else:
        return 'app-sidebar', 'app-content', {'collapsed': False}

# Callback for AI mode indicator update
@app.callback(
    Output('ai-mode-indicator', 'children'),
    Output('ai-mode-store', 'data'),
    Input('ai-mode-dropdown', 'value')
)
def update_ai_mode(mode):
    """Update AI mode indicator badge and store"""
    mode_labels = {
        'ai-assisted': 'ASSISTED',
        'ai-augmented': 'AUGMENTED',
        'ai-automated': 'AUTOMATED'
    }
    return mode_labels.get(mode, 'ASSISTED'), mode

# Callback for page routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to different page layouts based on URL"""
    if pathname == '/':
        return dashboard_layout
    elif pathname == '/projects':
        return projects_layout
    elif pathname == '/decision-tree' or pathname == '/screening':
        return decision_tree_layout
    elif pathname == '/markov' or pathname == '/quality':
        return markov_layout
    elif pathname == '/psm' or pathname == '/extraction':
        return psm_layout
    elif pathname == '/compare' or pathname == '/synthesis':
        return compare_layout
    elif pathname == '/dsa' or pathname == '/report':
        return dsa_layout
    elif pathname == '/psa' or pathname == '/settings':
        return psa_layout
    elif pathname in ['/protocol', '/literature']:
        return html.Div([
            html.H2(f"{pathname[1:].title()} Page", className="text-center mt-5"),
            html.P("This page is under construction.", className="text-center text-muted"),
            dbc.Button("Go Home", href="/", color="danger", className="mt-3")
        ], className="text-center")
    else:
        return html.Div([
            html.H1("404: Page Not Found", className="text-center mt-5"),
            dbc.Button("Go Home", href="/", color="danger", className="mt-3")
        ], className="text-center")

# Register all callbacks from modules
projects_callbacks(app)
decision_tree_callbacks(app)
markov_callbacks(app)
psm_callbacks(app)
compare_callbacks(app)
dsa_callbacks(app)
psa_callbacks(app)

if __name__ == '__main__':
    print(f"🚀 Starting Health Economic Modeling Hub on {HOST}:{PORT}")
    print(f"📊 Dashboard: http://{HOST}:{PORT}")
    app.run_server(host=HOST, port=PORT, debug=True)
