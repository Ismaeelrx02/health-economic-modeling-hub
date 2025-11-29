"""AI Mode Helper - Access current AI mode in callbacks"""

# AI Mode Descriptions
AI_MODES = {
    'ai-assisted': {
        'name': 'AI-Assisted',
        'icon': '🤝',
        'description': 'Manual control with AI suggestions and recommendations',
        'features': [
            'User inputs all parameters manually',
            'AI provides suggestions and validation',
            'AI highlights potential issues',
            'AI recommends parameter ranges',
            'User has full control over final decisions'
        ]
    },
    'ai-augmented': {
        'name': 'AI-Augmented',
        'icon': '⚡',
        'description': 'AI actively helps with tasks and automates repetitive work',
        'features': [
            'AI auto-fills common parameters',
            'AI suggests optimal parameter values',
            'AI performs sensitivity analysis automatically',
            'AI generates interim reports',
            'User reviews and approves AI suggestions'
        ]
    },
    'ai-automated': {
        'name': 'AI-Automated',
        'icon': '🤖',
        'description': 'Full AI control with minimal user intervention',
        'features': [
            'AI performs complete analysis pipeline',
            'AI selects models and parameters',
            'AI runs all sensitivity analyses',
            'AI generates final reports',
            'User only provides high-level objectives'
        ]
    }
}

def get_ai_mode_config(mode: str) -> dict:
    """Get configuration for specified AI mode"""
    return AI_MODES.get(mode, AI_MODES['ai-assisted'])

def should_auto_fill(mode: str) -> bool:
    """Check if AI should auto-fill parameters"""
    return mode in ['ai-augmented', 'ai-automated']

def should_auto_analyze(mode: str) -> bool:
    """Check if AI should automatically run analyses"""
    return mode == 'ai-automated'

def should_show_suggestions(mode: str) -> bool:
    """Check if AI should show suggestions"""
    return mode in ['ai-assisted', 'ai-augmented']

def should_validate_inputs(mode: str) -> bool:
    """Check if AI should validate inputs"""
    return True  # All modes validate

def get_ai_assistance_level(mode: str) -> str:
    """Get assistance level description"""
    levels = {
        'ai-assisted': 'Low - Suggestions only',
        'ai-augmented': 'Medium - Active help',
        'ai-automated': 'High - Full automation'
    }
    return levels.get(mode, 'Low')
