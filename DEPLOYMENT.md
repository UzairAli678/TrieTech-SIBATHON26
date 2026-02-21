# Deployment Guide for Streamlit Cloud

## 🚀 How to Deploy on Streamlit Cloud

### Step 1: Prepare Your Repository
1. Make sure all your code is pushed to GitHub
2. Ensure `.env` and `.streamlit/secrets.toml` are in `.gitignore` (already done)

### Step 2: Get Your API Keys
You'll need the following API keys:

- **Groq API Key** (FREE & Recommended) - Get from: https://console.groq.com/keys
- **Geoapify API Key** (FREE) - Get from: https://www.geoapify.com/
- **Exchangerate API Key** (FREE) - Get from: https://exchangerate.host/#pricing
- **Gemini API Key** (Optional) - Get from: https://makersuite.google.com/app/apikey

### Step 3: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Click "Advanced settings"

### Step 4: Add Secrets in Streamlit Cloud
In the "Secrets" section, paste the following (replace with your actual keys):

```toml
# Exchangerate.host API Key
EXCHANGERATE_API_KEY = "your_exchangerate_api_key_here"

# Geoapify API Key
GEOAPIFY_API_KEY = "your_geoapify_api_key_here"

# Groq API Key (FREE & FAST!)
GROQ_API_KEY = "your_groq_api_key_here"

# Google Gemini API Key (Optional)
GEMINI_API_KEY = "your_gemini_api_key_here"

# OpenAI API Key (Optional)
OPENAI_API_KEY = ""

# Map API Key (Optional)
MAP_API_KEY = ""

# Application Environment
APP_ENV = "production"
DEBUG = "False"
```

### Step 5: Deploy!
Click "Deploy" and wait for your app to build and launch.

---

## 💻 Local Development

### Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 🔒 How the Secrets System Works

The application uses a unified secrets management system that automatically works for both:

### Local Development
- Reads from `.env` file using `python-dotenv`
- Uses `os.getenv()` to access secrets

### Streamlit Cloud
- Reads from `st.secrets` (configured in dashboard)
- No code changes needed!

The `config/secrets_manager.py` module handles this automatically:

```python
from config.secrets_manager import GROQ_API_KEY, GEOAPIFY_API_KEY
# These work everywhere!
```

---

## 📝 Important Notes

1. **Never commit secrets** to Git:
   - `.env` is in `.gitignore`
   - `.streamlit/secrets.toml` is in `.gitignore`

2. **API Key Priority**:
   - Streamlit Cloud: Uses `st.secrets` first
   - Local: Falls back to `.env` file

3. **Testing Locally Before Deploy**:
   - Create `.streamlit/secrets.toml` locally (already done)
   - This simulates Streamlit Cloud environment
   - If it works locally with secrets.toml, it'll work on Cloud!

---

## ✅ Verification

To verify everything is working:

1. **Check API Keys Loading**:
   - Run the app locally
   - Check the AI Assistant page
   - Try the Tourist Attractions page
   - Use the Currency Converter

2. **All features should work**:
   - ✅ Currency conversion
   - ✅ AI chatbot responses
   - ✅ Tourist attractions map
   - ✅ Budget calculations

---

## 🐛 Troubleshooting

### "API key not found" error:
- **Local**: Check your `.env` file has the correct key names
- **Cloud**: Check your Streamlit Cloud secrets configuration

### "Module not found" error:
- Make sure all dependencies are in `requirements.txt`
- Check Python version compatibility (3.8+)

### API not responding:
- Verify your API keys are valid and active
- Check API rate limits
- Try using different API keys

---

## 📞 Support

For issues or questions:
1. Check the error message carefully
2. Verify API keys are correctly configured
3. Check Python and dependency versions
4. Review Streamlit Cloud logs (if deployed)
