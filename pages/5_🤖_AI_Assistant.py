"""
TriEtech AI Travel Assistant
Professional multilingual AI-powered travel guidance system
"""

import streamlit as st
from datetime import datetime
from utils.ai_assistant import get_ai_response
from utils.budget import fetch_countries
import time

st.set_page_config(page_title="TriEtech AI Assistant", page_icon="🧳", layout="wide")

# Initialize theme from main app
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Dynamic theming
theme = st.session_state.theme
if theme == "dark":
    bg_color = "#0E1117"
    secondary_bg = "#1E2530"
    card_bg = "#262C3A"
    text_color = "#FFFFFF"
    text_secondary = "#B0B8C5"
    border_color = "#3A4052"
    msg_bg = "#1E2530"
    shadow = "rgba(0, 0, 0, 0.5)"
else:
    bg_color = "#FFFFFF"
    secondary_bg = "#F7F9FC"
    card_bg = "#FFFFFF"
    text_color = "#1A202C"
    text_secondary = "#4A5568"
    border_color = "#E2E8F0"
    msg_bg = "#F7F9FC"
    shadow = "rgba(0, 0, 0, 0.1)"

# Enhanced Custom CSS for professional chat interface
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {bg_color};
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: {secondary_bg};
        border-right: 1px solid {border_color};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    
    /* Header Styling */
    header[data-testid="stHeader"] {{
        background: {secondary_bg};
        border-bottom: 1px solid {border_color};
    }}
    
    .main-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
    }}
    
    .main-header h1 {{
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }}
    
    .main-header p {{
        margin: 1rem 0 0 0;
        font-size: 1.25rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }}
    
    .user-message {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 20px 20px 4px 20px;
        margin: 1rem 0;
        margin-left: 20%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }}
    
    .assistant-message {{
        background: {msg_bg};
        color: {text_color};
        padding: 1rem 1.25rem;
        border-radius: 20px 20px 20px 4px;
        margin: 1rem 0;
        margin-right: 20%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        animation: slideInLeft 0.3s ease-out;
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    .timestamp {{
        font-size: 0.75rem;
        opacity: 0.6;
        margin-top: 0.5rem;
        font-weight: 500;
    }}
    
    .typing-indicator {{
        background: {msg_bg};
        padding: 1rem 1.25rem;
        border-radius: 20px;
        margin: 1rem 0;
        margin-right: 20%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        display: inline-block;
    }}
    
    .typing-indicator span {{
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #667eea;
        margin: 0 3px;
        animation: typing 1.4s infinite;
    }}
    
    .typing-indicator span:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    
    .typing-indicator span:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    
    @keyframes typing {{
        0%, 60%, 100% {{
            transform: translateY(0);
            opacity: 0.3;
        }}
        30% {{
            transform: translateY(-12px);
            opacity: 1;
        }}
    }}
    
    .info-card {{
        background: {card_bg};
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }}
    
    .info-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }}
    
    .stat-box {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.25rem;
        border-radius: 14px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stat-box:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(102, 126, 234, 0.4);
    }}
    
    .stat-box h3 {{
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
    }}
    
    .stat-box p {{
        margin: 0.5rem 0 0 0;
        font-size: 0.875rem;
        opacity: 0.95;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    div.stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
    }}
    
    /* Hide Main Menu */
    #MainMenu {{visibility: hidden;}}
    
    /* Footer */
    footer {{
        visibility: visible !important;
        background: {secondary_bg};
        border-top: 1px solid {border_color};
        padding: 1.5rem 0;
        margin-top: 3rem;
    }}
    
    footer * {{
        color: {text_secondary} !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {secondary_bg};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: #667eea;
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #764ba2;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>TriEtech AI Travel Assistant</h1>
    <p>Professional multilingual travel guidance powered by advanced AI</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
    
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"
    
if "countries_list" not in st.session_state:
    st.session_state.countries_list = None
    
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# Load countries
if st.session_state.countries_list is None:
    with st.spinner("Loading countries data..."):
        st.session_state.countries_list = fetch_countries()

countries = st.session_state.countries_list

# Sidebar - Settings
with st.sidebar:
    st.markdown("### Settings")
    
    # Language Selection
    languages = ["English", "Urdu", "Arabic", "French", "Spanish", "Chinese"]
    selected_language = st.selectbox(
        "Response Language",
        languages,
        index=languages.index(st.session_state.selected_language),
        help="AI will respond in your selected language"
    )
    
    if selected_language != st.session_state.selected_language:
        st.session_state.selected_language = selected_language
    
    # Country Selection
    st.markdown("### Travel Context")
    
    country_options = ["None (General Travel)"] + [f"{c['flag']} {c['name']}" for c in countries]
    
    selected_country_display = st.selectbox(
        "Select Destination",
        country_options,
        help="AI will provide context-specific advice for selected country"
    )
    
    if selected_country_display == "None (General Travel)":
        st.session_state.selected_country = None
        st.info("General travel mode - Ask anything!")
    else:
        country_name = selected_country_display.split(" ", 1)[1]
        st.session_state.selected_country = country_name
        st.success(f"Context: {selected_country_display}")
    
    # Chat Stats
    st.markdown("---")
    st.markdown("### Chat Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <h3>{len(st.session_state.chat_history)}</h3>
            <p>Messages</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <h3>{st.session_state.selected_language[:2]}</h3>
            <p>Language</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Clear Chat Button
    st.markdown("---")
    if st.button("Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.chat_history = []
        st.session_state.message_count = 0
        st.rerun()
    
    # Quick Questions
    st.markdown("---")
    st.markdown("### Quick Questions")
    
    quick_questions = [
        "What are the must-visit places?",
        "Best food to try?",
        "Budget travel tips?",
        "Safety advice?",
        "Best time to visit?",
        "Hotel recommendations?",
        "Local customs?",
        "Hidden gems?"
    ]
    
    for question in quick_questions:
        if st.button(question, key=f"q_{question}", use_container_width=True):
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": question,
                "timestamp": datetime.now()
            })
            st.session_state.message_count += 1
            st.rerun()

# Main chat area
st.markdown("### Chat")

# Display chat history
chat_container = st.container()

with chat_container:
    if len(st.session_state.chat_history) == 0:
        # Welcome message
        st.markdown("""
        <div class="info-card">
            <h2 style="color: #667eea; margin-top: 0;">Welcome to TriEtech AI Travel Assistant</h2>
            <p style="font-size: 1.1rem; color: #4a5568;">Your professional multilingual travel companion powered by advanced AI technology.</p>
            
            <h3 style="color: #2d3748; margin-top: 30px;">Our Services</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">
                <div style="padding: 15px; background: #f7fafc; border-radius: 8px; border-left: 3px solid #667eea;">
                    <strong>Tourist Attractions</strong><br/>
                    <span style="color: #718096;">Famous landmarks and hidden gems</span>
                </div>
                <div style="padding: 15px; background: #f7fafc; border-radius: 8px; border-left: 3px solid #667eea;">
                    <strong>Accommodation</strong><br/>
                    <span style="color: #718096;">Hotels and budget options</span>
                </div>
                <div style="padding: 15px; background: #f7fafc; border-radius: 8px; border-left: 3px solid #667eea;">
                    <strong>Food & Dining</strong><br/>
                    <span style="color: #718096;">Local cuisine recommendations</span>
                </div>
                <div style="padding: 15px; background: #f7fafc; border-radius: 8px; border-left: 3px solid #667eea;">
                    <strong>Budget Planning</strong><br/>
                    <span style="color: #718096;">Cost estimates and tips</span>
                </div>
                <div style="padding: 15px; background: #f7fafc; border-radius: 8px; border-left: 3px solid #667eea;">
                    <strong>Safety & Health</strong><br/>
                    <span style="color: #718096;">Travel safety advice</span>
                </div>
                <div style="padding: 15px; background: #f7fafc; border-radius: 8px; border-left: 3px solid #667eea;">
                    <strong>Cultural Insights</strong><br/>
                    <span style="color: #718096;">Local traditions and customs</span>
                </div>
            </div>
            
            <h3 style="color: #2d3748; margin-top: 30px;">Getting Started</h3>
            <ol style="color: #4a5568; line-height: 1.8;">
                <li>Select your preferred <strong>response language</strong> from the sidebar</li>
                <li>Choose a <strong>destination country</strong> for personalized advice (optional)</li>
                <li>Type your question below or use quick questions</li>
            </ol>
            
            <div style="margin-top: 25px; padding: 15px; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-radius: 10px; border: 1px solid #667eea30;">
                <strong style="color: #667eea;">Pro Tip:</strong> <span style="color: #4a5568;">Be specific for better answers. Example: "What are the best budget hotels in Paris?" instead of just "hotels"</span>
            </div>
            
            <p style="text-align: center; margin-top: 30px; color: #718096; font-size: 0.9rem;">
                Powered by <strong>TriEtech</strong> | Advanced AI Technology
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display messages
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div>{msg['content']}</div>
                    <div class="timestamp">You • {msg['timestamp'].strftime('%I:%M %p')}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <div>{msg['content']}</div>
                    <div class="timestamp">TriEtech AI • {msg['timestamp'].strftime('%I:%M %p')}</div>
                </div>
                """, unsafe_allow_html=True)

# Check if we need to get AI response
if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
    # Show typing indicator
    with st.spinner(""):
        st.markdown("""
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
        """, unsafe_allow_html=True)
        
        # Small delay for realism
        time.sleep(0.5)
        
        # Get AI response
        user_message = st.session_state.chat_history[-1]["content"]
        
        # Prepare chat history for AI (exclude the last user message)
        chat_context = st.session_state.chat_history[:-1]
        
        ai_response = get_ai_response(
            user_message=user_message,
            country=st.session_state.selected_country,
            language=st.session_state.selected_language,
            chat_history=chat_context
        )
        
        # Add AI response to chat
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now()
        })
        
        st.rerun()

# Input area at bottom - using chat_input for auto-send on Enter
user_input = st.chat_input(
    placeholder="Ask me anything about travel... (Press Enter to send)",
    key="chat_input_field"
)

# Handle send - automatically triggers on Enter
if user_input and user_input.strip():
    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input.strip(),
        "timestamp": datetime.now()
    })
    st.session_state.message_count += 1
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; opacity: 0.7; font-size: 0.9rem;">
    <p>Powered by <b>TriEtech</b> • Professional AI Travel Solutions</p>
</div>
""", unsafe_allow_html=True)
