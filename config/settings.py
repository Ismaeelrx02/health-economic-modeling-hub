"""Configuration settings for the Dash application"""
import os

# Application Settings
APP_TITLE = "Health Economic Modeling Hub"
VERSION = "1.0.0"
HOST = os.getenv("HOST", "0.0.0.0")  # Use 0.0.0.0 for production
PORT = int(os.getenv("PORT", 8050))

# Theme Settings
THEME = {
    'primary_red': '#DC2626',
    'secondary_red': '#991B1B',
    'white': '#FFFFFF',
    'black': '#000000',
    'light_gray': '#F3F4F6',
    'medium_gray': '#6B7280',
    'dark_gray': '#374151'
}

# Database Settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///health_econ_hub.db")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 5))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 10))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", 30))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", 3600))

# AI Service Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

# Calculation Settings
DEFAULT_DISCOUNT_RATE = 0.03
DEFAULT_WTP_THRESHOLD = 50000.0
MAX_TIME_HORIZON = 100

# AI Mode Settings
DEFAULT_AI_MODE = 'ai-assisted'
AI_MODES = ['ai-assisted', 'ai-augmented', 'ai-automated']

# Chart Settings
CHART_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
}
