"""
Currency Converter Page
Real-time currency conversion with exchange rates
"""

import streamlit as st
from utils.currency import get_supported_currencies, get_currency_name, convert_currency

st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="wide")

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
    shadow = "rgba(0, 0, 0, 0.5)"
    hover_bg = "#323847"
else:
    bg_color = "#FFFFFF"
    secondary_bg = "#F7F9FC"
    card_bg = "#FFFFFF"
    text_color = "#1A202C"
    text_secondary = "#4A5568"
    border_color = "#E2E8F0"
    shadow = "rgba(0, 0, 0, 0.1)"
    hover_bg = "#EDF2F7"

# Premium CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {bg_color};
        color: {text_color};
    }}
    
    h1, h2, h3 {{
        color: {text_color};
        font-weight: 700;
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
    
    /* Cards */
    .stAlert {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
    }}
    
    /* Buttons */
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

st.title("💱 Currency Converter")
st.markdown("Real-time exchange rates powered by exchangerate.host API")
st.markdown("---")

# Main converter section
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown("### From")
    from_currency = st.selectbox(
        "Select Currency",
        options=get_supported_currencies(),
        format_func=lambda x: f"{x} - {get_currency_name(x)}",
        index=get_supported_currencies().index("USD"),
        key="from"
    )
    amount = st.number_input(
        "Amount",
        min_value=0.01,
        value=100.0,
        step=10.0,
        format="%.2f"
    )

with col2:
    st.markdown("<div style='padding-top: 60px; text-align: center; font-size: 36px;'>→</div>",
                unsafe_allow_html=True)

with col3:
    st.markdown("### To")
    to_currency = st.selectbox(
        "Select Currency",
        options=get_supported_currencies(),
        format_func=lambda x: f"{x} - {get_currency_name(x)}",
        index=get_supported_currencies().index("EUR"),
        key="to"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Convert button
if st.button("🔄 Convert Currency", type="primary", use_container_width=True):
    with st.spinner("Converting..."):
        result = convert_currency(amount, from_currency, to_currency)
        
        if result:
            st.success("✅ Conversion Successful!")
            
            # Display converted amount prominently
            converted_amt = result['converted_amount']
            
            # Result card with converted amount
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; border-radius: 15px; text-align: center; color: white; margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                <h1 style='color: white; margin: 0; font-size: 48px; font-weight: bold;'>{converted_amt:,.2f} {to_currency}</h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 20px; margin-top: 15px;'>{amount:,.2f} {from_currency} =</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Exchange rate details
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric(
                    label="Exchange Rate",
                    value=f"{result['rate']:.6f}"
                )
            
            with col_b:
                st.metric(
                    label="Inverse Rate",
                    value=f"{1/result['rate']:.6f}"
                )
            
            with col_c:
                st.metric(
                    label="Last Updated",
                    value=result['timestamp'].split()[1]
                )
            
            # Additional info
            st.info(f"📅 Date: {result['date']} | 🕐 Time: {result['timestamp']}")
            
        else:
            st.error("❌ Conversion failed. Please check your internet connection and try again.")

st.markdown("---")

# Quick reference section
st.subheader("📊 Quick Reference")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    **Popular Currency Pairs:**
    - USD/EUR - US Dollar to Euro
    - GBP/USD - British Pound to US Dollar
    - USD/JPY - US Dollar to Japanese Yen
    - EUR/GBP - Euro to British Pound
    - AUD/USD - Australian Dollar to US Dollar
    """)

with col_info2:
    st.markdown("""
    **Tips:**
    - Exchange rates update in real-time
    - Rates may vary from your bank or exchange service
    - Consider transaction fees when exchanging
    - Use for reference purposes
    - Bookmark for quick access
    """)