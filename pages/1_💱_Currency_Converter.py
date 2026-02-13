"""
Currency Converter Page
Real-time currency conversion with exchange rates
"""

import streamlit as st
from utils.currency import get_supported_currencies, get_currency_name, convert_currency

st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="wide")

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
            
            # Result card
            st.markdown("""
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    margin: 20px 0;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                '>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<h1 style='color: white; margin: 0;'>{result['converted_amount']:,.2f} {to_currency}</h1>",
                       unsafe_allow_html=True)
            st.markdown(f"<p style='color: rgba(255,255,255,0.9); font-size: 18px;'>{amount:,.2f} {from_currency}</p>",
                       unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
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