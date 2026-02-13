"""
Application Configuration Settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MAP_API_KEY = os.getenv("MAP_API_KEY", "")
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY", "")  # Add your exchangerate.host API key here

# Application Settings
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

# Database Configuration (Optional)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/travel_planner.db")

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
