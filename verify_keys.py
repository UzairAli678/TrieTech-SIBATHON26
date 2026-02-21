"""
API Keys Verification Script
Run this to check if your API keys are properly configured
"""

from config.secrets_manager import (
    EXCHANGERATE_API_KEY,
    GEOAPIFY_API_KEY,
    GEMINI_API_KEY,
    GROQ_API_KEY,
    OPENAI_API_KEY,
    MAP_API_KEY,
    APP_ENV,
    DEBUG
)

def mask_key(key: str) -> str:
    """Mask API key for secure display"""
    if not key:
        return "❌ NOT SET"
    if len(key) < 8:
        return "✅ SET (too short to mask)"
    return f"✅ SET ({key[:4]}...{key[-4:]})"

print("=" * 60)
print("🔐 API Keys Configuration Check")
print("=" * 60)
print()
print(f"📍 Environment: {APP_ENV}")
print(f"🐛 Debug Mode: {DEBUG}")
print()
print("🔑 API Keys Status:")
print("-" * 60)
print(f"💱 EXCHANGERATE_API_KEY: {mask_key(EXCHANGERATE_API_KEY)}")
print(f"🗺️  GEOAPIFY_API_KEY:     {mask_key(GEOAPIFY_API_KEY)}")
print(f"🤖 GROQ_API_KEY:         {mask_key(GROQ_API_KEY)}")
print(f"✨ GEMINI_API_KEY:       {mask_key(GEMINI_API_KEY)}")
print(f"🔓 OPENAI_API_KEY:       {mask_key(OPENAI_API_KEY)}")
print(f"🗺️  MAP_API_KEY:          {mask_key(MAP_API_KEY)}")
print()
print("=" * 60)
print()

# Check critical keys
critical_keys = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "GEOAPIFY_API_KEY": GEOAPIFY_API_KEY,
    "EXCHANGERATE_API_KEY": EXCHANGERATE_API_KEY
}

missing_critical = [name for name, value in critical_keys.items() if not value]

if missing_critical:
    print("⚠️  WARNING: Critical API keys are missing!")
    print("Missing keys:", ", ".join(missing_critical))
    print()
    print("Please add these keys to:")
    print("  - Local: .env file or .streamlit/secrets.toml")
    print("  - Cloud: Streamlit Cloud secrets (in app settings)")
    print()
else:
    print("✅ All critical API keys are configured!")
    print("🚀 Your application is ready to use!")
    print()

print("=" * 60)
