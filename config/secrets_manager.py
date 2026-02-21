"""
Secrets Manager - Works for both local development and Streamlit Cloud
Handles API keys and sensitive configuration seamlessly
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()


def get_secret(key: str, default: str = "") -> str:
    """
    Get secret value from environment or Streamlit secrets
    
    This function works for both:
    - Local development: Reads from .env file via os.getenv()
    - Streamlit Cloud: Reads from st.secrets
    
    Args:
        key: Secret key name (e.g., "GROQ_API_KEY")
        default: Default value if key not found
        
    Returns:
        Secret value as string
    """
    # Try Streamlit secrets first (for cloud deployment)
    try:
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except (FileNotFoundError, KeyError):
        pass
    
    # Fall back to environment variable (for local development)
    return os.getenv(key, default)


# Pre-load all API keys
EXCHANGERATE_API_KEY = get_secret("EXCHANGERATE_API_KEY")
GEOAPIFY_API_KEY = get_secret("GEOAPIFY_API_KEY")
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
GROQ_API_KEY = get_secret("GROQ_API_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
MAP_API_KEY = get_secret("MAP_API_KEY")

# Application Settings
APP_ENV = get_secret("APP_ENV", "development")
DEBUG = get_secret("DEBUG", "True") == "True"

# Database Configuration
DATABASE_URL = get_secret("DATABASE_URL", "sqlite:///data/travel_planner.db")
