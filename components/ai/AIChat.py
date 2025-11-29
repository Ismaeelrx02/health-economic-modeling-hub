"""Floating AI Chat Button and Dialog Component"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_ai_chat_button():
    """
    Create floating AI chat button (bottom-right corner).
    Returns the button component and modal dialog.
    """
    
    # Floating button (bottom-right) - Icon only
    chat_button = html.Div(
        dbc.Button(
            html.I(className="fas fa-robot", style={'fontSize': '24px'}),
            id="ai-chat-button",
            color="primary",
            size="lg",
            className="shadow-lg",
            style={
                'borderRadius': '50%',
                'width': '60px',
                'height': '60px',
                'padding': '0',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            }
        ),
        style={
            'position': 'fixed',
            'bottom': '30px',
            'right': '30px',
            'zIndex': '1000',
            'cursor': 'pointer'
        }
    )
    
    # Chat modal dialog - Clean, minimal
    chat_modal = dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle("AI Assistant"),
                close_button=True
            ),
            dbc.ModalBody(
                [
                    # Chat messages container
                    html.Div(
                        id="ai-chat-messages",
                        children=[],
                        style={
                            'height': '400px',
                            'overflowY': 'auto',
                            'padding': '15px',
                            'backgroundColor': '#f8f9fa',
                            'borderRadius': '8px',
                            'marginBottom': '15px'
                        }
                    ),
                    # Input area
                    dbc.InputGroup(
                        [
                            dbc.Textarea(
                                id="ai-chat-input",
                                placeholder="Ask about health economic modeling...",
                                style={
                                    'resize': 'none',
                                    'minHeight': '60px'
                                },
                                n_submit=0
                            ),
                            dbc.Button(
                                html.I(className="fas fa-paper-plane"),
                                id="ai-chat-send",
                                color="primary",
                                n_clicks=0
                            )
                        ]
                    ),
                    # Loading indicator
                    dbc.Spinner(
                        html.Div(id="ai-chat-loading"),
                        size="sm",
                        color="primary",
                        type="border"
                    ),
                    # Status message
                    html.Div(id="ai-chat-status", className="mt-2 text-muted small")
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        [html.I(className="fas fa-trash me-2"), "Clear"],
                        id="ai-chat-clear",
                        color="secondary",
                        outline=True,
                        size="sm",
                        n_clicks=0
                    ),
                    dbc.Button(
                        "Close",
                        id="ai-chat-close",
                        color="secondary",
                        size="sm"
                    )
                ]
            )
        ],
        id="ai-chat-modal",
        size="lg",
        is_open=False,
        backdrop=True,
        scrollable=True
    )
    
    # Store for conversation history and provider
    conversation_store = dcc.Store(id='ai-conversation-history', data=[])
    provider_store = dcc.Store(id='ai-provider-store', data='openai')  # Auto-fallback handled in backend
    
    return html.Div([
        chat_button,
        chat_modal,
        conversation_store,
        provider_store
    ])


def format_chat_message(content: str, is_user: bool = True, timestamp: str = None):
    """
    Format a chat message for display.
    
    Args:
        content: Message content
        is_user: True if user message, False if AI message
        timestamp: Optional timestamp string
    
    Returns:
        Formatted message component
    """
    if is_user:
        return html.Div(
            [
                html.Div(
                    [
                        html.Strong("You", className="text-primary"),
                        html.Span(f" • {timestamp}" if timestamp else "", className="text-muted small")
                    ],
                    className="mb-1"
                ),
                html.Div(
                    content,
                    className="p-3 bg-primary text-white rounded",
                    style={'marginLeft': '20%'}
                )
            ],
            className="mb-3 text-end"
        )
    else:
        return html.Div(
            [
                html.Div(
                    [
                        html.I(className="fas fa-robot text-success me-2"),
                        html.Strong("AI Assistant", className="text-success"),
                        html.Span(f" • {timestamp}" if timestamp else "", className="text-muted small")
                    ],
                    className="mb-1"
                ),
                html.Div(
                    dcc.Markdown(
                        content,
                        className="p-3 bg-white border rounded",
                        style={
                            'marginRight': '20%',
                            'whiteSpace': 'pre-wrap'
                        }
                    )
                )
            ],
            className="mb-3"
        )
