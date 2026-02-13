"""
Travel Budget Planner - Main Application
A comprehensive fintech travel planning application with AI assistance
"""

import streamlit as st
from config.settings import PAGE_CONFIG, THEME_CONFIG

# Page configuration
st.set_page_config(
    page_title=PAGE_CONFIG["title"],
    page_icon=PAGE_CONFIG["icon"],
    layout=PAGE_CONFIG["layout"],
    initial_sidebar_state=PAGE_CONFIG["initial_sidebar_state"]
)

# Custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css()
except FileNotFoundError:
    pass  # CSS file is optional

# Main page content
def main():
    st.title("🌍 Travel Budget Planner")
    st.markdown("---")
    
    # Welcome section
    st.header("Welcome to Your Personal Travel Finance Assistant!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Features
        
        - **💱 Currency Converter**: Real-time exchange rates
        - **💰 Budget Calculator**: Plan your trip expenses
        - **📊 Dashboard**: Visualize your spending patterns
        - **🗺️ Tourist Attractions**: Discover popular destinations
        - **🤖 AI Assistant**: Get personalized travel advice
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Getting Started
        
        1. Navigate using the sidebar
        2. Convert currencies for your destination
        3. Create a detailed budget plan
        4. Explore attractions on the map
        5. Chat with our AI assistant for tips
        """)
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📈 Quick Overview")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Supported Currencies", "150+", "💱")
    
    with metric_col2:
        st.metric("Budget Templates", "10+", "📝")
    
    with metric_col3:
        st.metric("Countries", "195", "🌎")
    
    with metric_col4:
        st.metric("AI Powered", "✓", "🤖")
    
    st.markdown("---")
    
    # Information section
    st.info("""
    👈 **Use the sidebar to navigate** between different features of the app.
    Start by converting currencies or creating a budget plan!
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Streamlit | © 2026 Travel Budget Planner</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
