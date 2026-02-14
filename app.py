"""
TriEtech Travel Intelligence Dashboard
Professional AI-powered travel planning and budgeting platform
"""

import streamlit as st
from config.settings import PAGE_CONFIG, THEME_CONFIG

# Page configuration
st.set_page_config(
    page_title="TriEtech Travel Dashboard",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "sidebar_expanded" not in st.session_state:
    st.session_state.sidebar_expanded = True

# Premium Custom CSS with Dark/Light Mode
def apply_premium_styling():
    if st.session_state.theme == "dark":
        primary_bg = "#0E1117"
        secondary_bg = "#1E2530"
        card_bg = "#262C3A"
        text_primary = "#FFFFFF"
        text_secondary = "#B0B8C5"
        accent_color = "#667EEA"
        accent_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        border_color = "#3A4052"
        shadow = "rgba(0, 0, 0, 0.5)"
        hover_bg = "#323847"
    else:
        primary_bg = "#FFFFFF"
        secondary_bg = "#F7F9FC"
        card_bg = "#FFFFFF"
        text_primary = "#1A202C"
        text_secondary = "#4A5568"
        accent_color = "#667EEA"
        accent_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        border_color = "#E2E8F0"
        shadow = "rgba(0, 0, 0, 0.1)"
        hover_bg = "#EDF2F7"
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Global Styles */
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* Main App Background */
        .stApp {{
            background: {primary_bg};
            color: {text_primary};
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background: {secondary_bg};
            border-right: 1px solid {border_color};
            box-shadow: 4px 0 20px {shadow};
        }}
        
        [data-testid="stSidebar"] > div:first-child {{
            background: {secondary_bg};
        }}
        
        /* Sidebar Text and Labels */
        [data-testid="stSidebar"] * {{
            color: {text_primary} !important;
        }}
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {{
            color: {text_primary};
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: {text_primary};
        }}
        
        /* Sidebar Navigation Items */
        [data-testid="stSidebarNav"] {{
            padding-top: 2rem;
        }}
        
        [data-testid="stSidebarNav"] ul {{
            padding: 0 1rem;
        }}
        
        [data-testid="stSidebarNav"] li {{
            margin-bottom: 0.5rem;
        }}
        
        [data-testid="stSidebarNav"] a {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 0.875rem 1rem;
            color: {text_primary} !important;
            text-decoration: none;
            display: flex;
            align-items: center;
            font-weight: 500;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px {shadow};
        }}
        
        [data-testid="stSidebarNav"] a:hover {{
            background: {hover_bg};
            transform: translateX(8px);
            box-shadow: 0 4px 16px {shadow};
            border-color: {accent_color};
        }}
        
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: {accent_gradient};
            color: white !important;
            font-weight: 600;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        }}
        
        /* Header Styling */
        header[data-testid="stHeader"] {{
            background: {secondary_bg};
            border-bottom: 1px solid {border_color};
            box-shadow: 0 2px 8px {shadow};
        }}
        
        /* Footer Styling */
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
        
        /* Premium Card Design */
        .premium-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px {shadow};
            transition: all 0.3s ease;
        }}
        
        .premium-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px {shadow};
        }}
        
        /* Hero Section */
        .hero-section {{
            background: {accent_gradient};
            padding: 4rem 2rem;
            border-radius: 24px;
            text-align: center;
            margin-bottom: 3rem;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .hero-section::before {{
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
        
        .hero-title {{
            font-size: 3.5rem;
            font-weight: 800;
            color: white;
            margin: 0;
            text-shadow: 0 4px 20px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }}
        
        .hero-subtitle {{
            font-size: 1.25rem;
            color: rgba(255,255,255,0.95);
            margin-top: 1rem;
            position: relative;
            z-index: 1;
        }}
        
        /* Feature Grid */
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .feature-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 1.875rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px {shadow};
        }}
        
        .feature-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 32px {shadow};
            border-color: {accent_color};
        }}
        
        .feature-icon {{
            width: 56px;
            height: 56px;
            background: {accent_gradient};
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        }}
        
        .feature-title {{
            font-size: 1.25rem;
            font-weight: 700;
            color: {text_primary};
            margin-bottom: 0.75rem;
        }}
        
        .feature-description {{
            color: {text_secondary};
            line-height: 1.6;
            font-size: 0.95rem;
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            font-size: 2.5rem;
            font-weight: 700;
            background: {accent_gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {text_secondary};
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: {accent_gradient};
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.875rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
        }}
        
        /* Toggle Switch */
        .theme-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 999;
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 50px;
            padding: 0.5rem 1rem;
            box-shadow: 0 4px 16px {shadow};
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .theme-toggle:hover {{
            box-shadow: 0 8px 24px {shadow};
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: {text_primary};
            font-weight: 700;
        }}
        
        /* Text */
        p {{
            color: {text_secondary};
            line-height: 1.7;
        }}
        
        /* Divider */
        hr {{
            border: none;
            border-top: 1px solid {border_color};
            margin: 2rem 0;
        }}
        
        /* Info Box */
        .stAlert {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 1.25rem;
        }}
        
        /* Hide Streamlit Main Menu */
        #MainMenu {{visibility: hidden;}}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {secondary_bg};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {accent_color};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #764ba2;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_premium_styling()

# Main page content
def main():
    # Theme Toggle in Sidebar
    with st.sidebar:
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Theme:** {'🌙 Dark Mode' if st.session_state.theme == 'dark' else '☀️ Light Mode'}")
        with col2:
            if st.button("🔄", key="theme_toggle", help="Toggle theme"):
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 1rem; opacity: 0.7;'>
            <p style='font-size: 0.75rem; margin: 0;'>© 2026 TriEtech</p>
            <p style='font-size: 0.7rem; margin: 0.25rem 0 0 0;'>Travel Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">TriEtech Travel Intelligence</h1>
        <p class="hero-subtitle">Enterprise-Grade Travel Planning & Budgeting Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome Message
    st.markdown("""
    <div class="premium-card">
        <h2 style='margin-top: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Welcome to TriEtech Platform
        </h2>
        <p style='font-size: 1.1rem; line-height: 1.8;'>
            Experience the next generation of travel planning with our AI-powered intelligence platform. 
            Seamlessly manage budgets, explore destinations, and get personalized travel insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("## Platform Features")
    st.markdown("<br>", unsafe_allow_html=True)
    
    features = [
        {
            "icon": "💱",
            "title": "Currency Converter",
            "description": "Real-time exchange rates for 150+ global currencies with advanced conversion tools and historical data tracking."
        },
        {
            "icon": "💰",
            "title": "Budget Calculator",
            "description": "Comprehensive trip expense planning with detailed breakdowns, category management, and smart recommendations."
        },
        {
            "icon": "📊",
            "title": "Analytics Dashboard",
            "description": "Advanced spending pattern visualization with interactive charts, trends analysis, and predictive insights."
        },
        {
            "icon": "🗺️",
            "title": "Tourist Attractions",
            "description": "Interactive destination explorer with verified locations, detailed information, and smart mapping technology."
        },
        {
            "icon": "🤖",
            "title": "AI Travel Assistant",
            "description": "Multilingual AI-powered guidance providing personalized recommendations and 24/7 travel support."
        },
        {
            "icon": "🔒",
            "title": "Enterprise Security",
            "description": "Bank-level encryption and data protection ensuring your travel information remains private and secure."
        }
    ]
    
    # Display features in grid
    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(features):
                feature = features[i + j]
                with col:
                    st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{feature['icon']}</div>
                        <div class="feature-title">{feature['title']}</div>
                        <div class="feature-description">{feature['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Platform Statistics
    st.markdown("## Platform Statistics")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Currencies", "150+", "Global coverage")
    
    with col2:
        st.metric("Countries", "195", "Destinations")
    
    with col3:
        st.metric("Templates", "10+", "Budget plans")
    
    with col4:
        st.metric("AI Models", "Advanced", "Multi-lingual")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Getting Started Section
    st.markdown("## Quick Start Guide")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style='margin-top: 0;'>For First-Time Users</h3>
            <ol style='line-height: 2;'>
                <li><strong>Explore Navigation:</strong> Use the sidebar to access all features</li>
                <li><strong>Set Budget:</strong> Start with the Budget Calculator</li>
                <li><strong>Convert Currency:</strong> Check exchange rates for your destination</li>
                <li><strong>Discover Places:</strong> Browse tourist attractions interactively</li>
                <li><strong>Get AI Help:</strong> Chat with our multilingual assistant</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style='margin-top: 0;'>Pro Tips</h3>
            <ul style='line-height: 2;'>
                <li><strong>Theme Toggle:</strong> Switch between dark and light modes in the sidebar</li>
                <li><strong>Real-Time Data:</strong> All currency rates are updated live</li>
                <li><strong>AI Context:</strong> Select a country for personalized AI recommendations</li>
                <li><strong>Multiple Languages:</strong> Get responses in 6 different languages</li>
                <li><strong>Export Data:</strong> Download your budgets and analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <p style='font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;'>
            Powered by <span style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>TriEtech</span>
        </p>
        <p style='opacity: 0.7; font-size: 0.9rem;'>
            Professional Travel Intelligence Platform | Enterprise Solutions | © 2026 All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
