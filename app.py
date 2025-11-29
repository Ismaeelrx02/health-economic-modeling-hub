"""
Health Economic Modeling Hub - Dash Application
Module-based architecture with integrated layouts and callbacks
Red, White, and Black color scheme with collapsible sidebar
"""
import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import logging

# Import configuration
from config.settings import THEME, APP_TITLE, PORT, HOST

# Initialize database
from database import init_db
from database.connection import dispose_db

# Import AI chat component
from components.ai.AIChat import create_ai_chat_button

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import modules (each has layout + callbacks together)
from modules.dashboard import layout as dashboard_layout
from modules.projects import layout as projects_layout, register_callbacks as projects_callbacks
from modules.decision_tree import layout as decision_tree_layout, register_callbacks as decision_tree_callbacks
from modules.markov import layout as markov_layout, register_callbacks as markov_callbacks
from modules.psm import layout as psm_layout, register_callbacks as psm_callbacks
from modules.input import layout as input_layout, register_callbacks as input_callbacks
from modules.base_case import layout as base_case_layout, register_callbacks as base_case_callbacks
from modules.dsa import layout as dsa_layout, register_callbacks as dsa_callbacks
from modules.psa import layout as psa_layout, register_callbacks as psa_callbacks
from modules.report import layout as report_layout, register_callbacks as report_callbacks

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

# Initialize database on startup
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

# App layout with collapsible sidebar and AI chat
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='ai-mode-store', data='ai-assisted'),  # Store AI mode globally
    dcc.Store(id='sidebar-state', data={'collapsed': False}),  # Store sidebar state
    
    # AI Chat Component (floating button + modal)
    create_ai_chat_button(),
    
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
                html.Button(
                    id='ai-mode-indicator',
                    className="ai-mode-badge",
                    children='ASSISTED',
                    n_clicks=0
                )
            ], className='header-right')
        ], className='header-content')
    ], className='app-header'),
    
    # Main container with sidebar and content
    html.Div([
        # Collapsible Sidebar (Red background)
        html.Div([
            html.Div([
                # Dashboard
                dbc.NavLink([
                    html.I(className="fas fa-tachometer-alt"),
                    html.Span("Dashboard", className='nav-text')
                ], href="/", id="nav-dashboard", className='nav-item'),
                
                # Projects
                dbc.NavLink([
                    html.I(className="fas fa-folder-open"),
                    html.Span("Projects", className='nav-text')
                ], href="/projects", id="nav-projects", className='nav-item'),
                
                # Model Setup Section
                html.Div([
                    html.Div([
                        html.I(className="fas fa-cogs me-2"),
                        html.Span("Model Setup", className='nav-text')
                    ], className='nav-section-header'),
                    
                    # Decision Tree
                    dbc.NavLink([
                        html.I(className="fas fa-code-branch"),
                        html.Span("Decision Tree", className='nav-text')
                    ], href="/decision-tree", id="nav-decision-tree", className='nav-item nav-sub-item'),
                    
                    # Markov Model
                    dbc.NavLink([
                        html.I(className="fas fa-circle-notch"),
                        html.Span("Markov Model", className='nav-text')
                    ], href="/markov", id="nav-markov", className='nav-item nav-sub-item'),
                    
                    # Partitioned Survival Model
                    dbc.NavLink([
                        html.I(className="fas fa-chart-area"),
                        html.Span("Partitioned Survival", className='nav-text')
                    ], href="/psm", id="nav-psm", className='nav-item nav-sub-item'),
                ], className='nav-section'),
                
                # Input
                dbc.NavLink([
                    html.I(className="fas fa-keyboard"),
                    html.Span("Input", className='nav-text')
                ], href="/input", id="nav-input", className='nav-item'),
                
                # Base Case Analysis
                dbc.NavLink([
                    html.I(className="fas fa-calculator"),
                    html.Span("Base Case Analysis", className='nav-text')
                ], href="/base-case", id="nav-base-case", className='nav-item'),
                
                # Sensitivity Analysis Section
                html.Div([
                    html.Div([
                        html.I(className="fas fa-adjust me-2"),
                        html.Span("Sensitivity Analysis", className='nav-text')
                    ], className='nav-section-header'),
                    
                    # Deterministic SA
                    dbc.NavLink([
                        html.I(className="fas fa-chart-bar"),
                        html.Span("Deterministic SA", className='nav-text')
                    ], href="/dsa", id="nav-dsa", className='nav-item nav-sub-item'),
                    
                    # Probabilistic SA
                    dbc.NavLink([
                        html.I(className="fas fa-dice-d20"),
                        html.Span("Probabilistic SA", className='nav-text')
                    ], href="/psa", id="nav-psa", className='nav-item nav-sub-item'),
                ], className='nav-section'),
                
                # Report
                dbc.NavLink([
                    html.I(className="fas fa-file-pdf"),
                    html.Span("Report", className='nav-text')
                ], href="/report", id="nav-report", className='nav-item'),
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

# Callback for AI mode indicator update - cycle through modes on click
@app.callback(
    [Output('ai-mode-indicator', 'children'),
     Output('ai-mode-store', 'data')],
    Input('ai-mode-indicator', 'n_clicks'),
    State('ai-mode-store', 'data')
)
def cycle_ai_mode(n_clicks, current_mode):
    """Cycle through AI modes on button click"""
    if n_clicks is None or n_clicks == 0:
        return 'ASSISTED', 'ai-assisted'
    
    modes = ['ai-assisted', 'ai-augmented', 'ai-automated']
    labels = {'ai-assisted': 'ASSISTED', 'ai-augmented': 'AUGMENTED', 'ai-automated': 'AUTOMATED'}
    
    # Get current index and cycle to next
    try:
        current_idx = modes.index(current_mode)
        next_idx = (current_idx + 1) % len(modes)
        next_mode = modes[next_idx]
        return labels[next_mode], next_mode
    except:
        return 'ASSISTED', 'ai-assisted'

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
    elif pathname == '/decision-tree':
        return decision_tree_layout
    elif pathname == '/markov':
        return markov_layout
    elif pathname == '/psm':
        return psm_layout
    elif pathname == '/input':
        return input_layout
    elif pathname == '/base-case':
        return base_case_layout
    elif pathname == '/dsa':
        return dsa_layout
    elif pathname == '/psa':
        return psa_layout
    elif pathname == '/report':
        return report_layout
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
input_callbacks(app)
base_case_callbacks(app)
dsa_callbacks(app)
psa_callbacks(app)
report_callbacks(app)

# ============= AI CHAT CALLBACKS =============

from services.ai_service import AIService
from components.ai.AIChat import format_chat_message
from datetime import datetime

# Initialize AI service with auto-fallback
ai_service = AIService()

@app.callback(
    Output('ai-chat-modal', 'is_open'),
    [Input('ai-chat-button', 'n_clicks'),
     Input('ai-chat-close', 'n_clicks')],
    [State('ai-chat-modal', 'is_open')]
)
def toggle_ai_modal(open_clicks, close_clicks, is_open):
    """Toggle AI chat modal"""
    if open_clicks or close_clicks:
        return not is_open
    return is_open

@app.callback(
    [Output('ai-chat-messages', 'children'),
     Output('ai-chat-input', 'value'),
     Output('ai-conversation-history', 'data'),
     Output('ai-chat-status', 'children')],
    [Input('ai-chat-send', 'n_clicks'),
     Input('ai-chat-input', 'n_submit'),
     Input('ai-chat-clear', 'n_clicks')],
    [State('ai-chat-input', 'value'),
     State('ai-conversation-history', 'data'),
     State('ai-chat-messages', 'children')],
    prevent_initial_call=True
)
def handle_chat(send_clicks, n_submit, clear_clicks, message, history, current_messages):
    """Handle chat interactions with auto-fallback between providers"""
    from dash import callback_context
    
    if not callback_context.triggered:
        return current_messages, '', history, ''
    
    trigger = callback_context.triggered[0]['prop_id']
    
    # Clear chat
    if 'clear' in trigger:
        return [], '', [], 'Chat history cleared'
    
    # Send message
    if ('send' in trigger or 'submit' in trigger) and message and message.strip():
        # Use global AI service with auto-fallback
        global ai_service
        if not ai_service.is_available():
            ai_service = AIService()  # Reinitialize with fallback
        
        # Check if service is available
        if not ai_service.is_available():
            error_msg = format_chat_message(
                "⚠️ AI service is not configured. Please add your API key to environment variables:\n\n"
                "- For OpenAI: Set `OPENAI_API_KEY`\n"
                "- For Anthropic: Set `ANTHROPIC_API_KEY`",
                is_user=False,
                timestamp=datetime.now().strftime("%H:%M")
            )
            return current_messages + [error_msg], '', history, 'API key missing'
        
        # Add user message
        timestamp = datetime.now().strftime("%H:%M")
        user_msg = format_chat_message(message, is_user=True, timestamp=timestamp)
        
        # Get AI response with auto-fallback
        try:
            response = ai_service.chat(message, conversation_history=history)
            ai_msg = format_chat_message(response, is_user=False, timestamp=datetime.now().strftime("%H:%M"))
            
            # Update history
            new_history = history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ]
            
            provider_name = ai_service.provider.value.upper() if ai_service.provider else "AI"
            return current_messages + [user_msg, ai_msg], '', new_history, f'Response from {provider_name}'
        
        except Exception as e:
            error_msg = format_chat_message(
                f"Sorry, I encountered an error: {str(e)}",
                is_user=False,
                timestamp=datetime.now().strftime("%H:%M")
            )
            return current_messages + [user_msg, error_msg], '', history, f'Error: {str(e)}'
    
    return current_messages, message, history, ''

# ============= END AI CHAT CALLBACKS =============

# Expose server for production deployment (Gunicorn, etc.)
server = app.server

if __name__ == '__main__':
    print(f"🚀 Starting Health Economic Modeling Hub on {HOST}:{PORT}")
    print(f"📊 Dashboard: http://{HOST}:{PORT}")
    print(f"🤖 AI Chat: Available")
    print(f"💾 Database: Initialized")
    
    try:
        app.run_server(host=HOST, port=PORT, debug=True)
    finally:
        # Clean up database connections on shutdown
        dispose_db()
        logger.info("Application shutdown complete")
