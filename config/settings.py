"""
Application Configuration Settings
"""

from config.secrets_manager import (
    EXCHANGERATE_API_KEY,
    GEOAPIFY_API_KEY,
    GEMINI_API_KEY,
    GROQ_API_KEY,
    OPENAI_API_KEY,
    MAP_API_KEY,
    APP_ENV,
    DEBUG,
    DATABASE_URL
)

# Page Configuration
PAGE_CONFIG = {
    "title": "Travel Budget Planner",
    "icon": "🌍",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Theme Configuration
THEME_CONFIG = {
    "primaryColor": "#FF4B4B",
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F0F2F6",
    "textColor": "#262730",
    "font": "sans serif"
}

# Export API Keys (already imported from secrets_manager)
# These will work for both local (.env) and cloud (st.secrets)

# Currency API Settings
CURRENCY_API_FALLBACK = "https://api.exchangerate-api.com/v4/latest/"

# Default Budget Categories
DEFAULT_BUDGET_CATEGORIES = [
    "Accommodation",
    "Transportation",
    "Food & Dining",
    "Entertainment",
    "Shopping",
    "Activities & Tours",
    "Emergency Fund",
    "Miscellaneous"
]

# Map Settings
DEFAULT_MAP_CENTER = [20.0, 0.0]  # World center
DEFAULT_MAP_ZOOM = 2

# AI Assistant Settings
AI_MODEL = "gpt-3.5-turbo"
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 500

# Session State Keys
SESSION_KEYS = {
    "budget_data": "budget_data",
    "currency_history": "currency_history",
    "chat_history": "chat_history",
    "selected_country": "selected_country"
}
