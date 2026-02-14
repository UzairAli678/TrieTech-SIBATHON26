"""
Budget Calculator Page - AI-Powered Professional Trip Budget Planner
Smart cost estimation with real-world data and intelligent suggestions
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.budget import (
    fetch_countries, 
    calculate_smart_budget, 
    generate_smart_suggestions,
    save_budget_history,
    get_breakdown_percentage,
    get_country_category
)

st.set_page_config(page_title="AI Budget Calculator", page_icon="💰", layout="wide")

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
else:
    bg_color = "#FFFFFF"
    secondary_bg = "#F7F9FC"
    card_bg = "#FFFFFF"
    text_color = "#1A202C"
    text_secondary = "#4A5568"
    border_color = "#E2E8F0"
    shadow = "rgba(0, 0, 0, 0.1)"

# Professional CSS Styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
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
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        animation: fadeInDown 0.8s ease-out;
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
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }}
    
    .main-header p {{
        margin: 1rem 0 0 0;
        font-size: 1.25rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }}
    
    .lifestyle-card {{
        background: {card_bg};
        border: 3px solid {border_color};
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        height: 100%;
        color: {text_color};
    }}
    
    .lifestyle-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.15);
        border-color: #667eea;
    }}
    
    .lifestyle-card.selected {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5);
    }}
    
    .lifestyle-icon {{
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .lifestyle-name {{
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }}
    
    .lifestyle-desc {{
        font-size: 0.9rem;
        opacity: 0.85;
    }}
    
    .cost-card {{
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        box-shadow: 0 12px 40px rgba(245, 87, 108, 0.4);
        animation: scaleIn 0.6s ease-out;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }}
    
    .cost-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(245, 87, 108, 0.5);
    }}
    
    .cost-amount {{
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }}
    
    .cost-label {{
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
        font-weight: 600;
    }}
    
    .info-card {{
        background: {card_bg};
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
        color: {text_color};
        transition: all 0.3s ease;
    }}
    
    .info-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }}
    
    .suggestion-card {{
        background: {card_bg};
        border-left: 5px solid;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        color: {text_color};
        transition: all 0.3s ease;
        gap: 1rem;
    }}
    
    .suggestion-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(0,0,0,0.12);
    }}
    
    .suggestion-icon {{
        font-size: 1.8rem;
        flex-shrink: 0;
    }}
    
    .suggestion-text {{
        flex-grow: 1;
        margin: 0;
        font-size: 0.95rem;
    }}
    
    .stat-box {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stat-box:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(102, 126, 234, 0.4);
    }}
    
    .stat-value {{
        font-size: 2.25rem;
        font-weight: 800;
        margin: 0;
    }}
    
    .stat-label {{
        font-size: 0.875rem;
        opacity: 0.95;
        margin-top: 0.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .country-badge {{
        display: inline-block;
        background: {card_bg};
        border: 2px solid {border_color};
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.3rem;
        color: {text_color};
        transition: all 0.3s ease;
    }}
    
    .country-badge:hover {{
        border-color: #667eea;
        transform: scale(1.05);
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
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes scaleIn {{
        from {{
            opacity: 0;
            transform: scale(0.8);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💰 AI-Powered Trip Budget Calculator</h1>
    <p>Smart cost estimation with real-world data • Professional planning made simple</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'countries' not in st.session_state:
    with st.spinner("🌍 Loading countries..."):
        st.session_state.countries = fetch_countries()

if 'selected_lifestyle' not in st.session_state:
    st.session_state.selected_lifestyle = "Standard"

# STEP 1: Country Selection
st.markdown("### 🌍 Step 1: Select Your Destination")

countries = st.session_state.countries
country_options = [f"{c['flag']} {c['name']}" for c in countries]

selected_country_display = st.selectbox(
    "Choose your travel destination",
    country_options,
    index=0,
    help="Select from 190+ countries worldwide"
)

# Extract country data
selected_idx = country_options.index(selected_country_display)
selected_country_data = countries[selected_idx]
country_name = selected_country_data['name']
currency = selected_country_data['currency']
flag = selected_country_data['flag']

# Display country info
st.markdown(f"""
<div class="info-card">
    <strong>{flag} {country_name}</strong><br>
    <span style="color: #666;">Currency: {currency} • Category: <strong>{get_country_category(country_name).upper()}</strong> cost destination</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# STEP 2: Trip Details
st.markdown("### 📅 Step 2: Trip Details")

col1, col2 = st.columns(2)

with col1:
    travelers = st.number_input(
        "👥 Number of Travelers",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        help="Total number of people traveling"
    )

with col2:
    days = st.number_input(
        "🗓️ Number of Days",
        min_value=1,
        max_value=365,
        value=7,
        step=1,
        help="Duration of your trip"
    )

st.markdown("<br>", unsafe_allow_html=True)

# STEP 3: Lifestyle Selection
st.markdown("### ✨ Step 3: Choose Your Travel Style")

lifestyle_col1, lifestyle_col2, lifestyle_col3 = st.columns(3)

lifestyles = {
    "Budget": {
        "icon": "🎒",
        "desc": "Hostels, street food, public transport"
    },
    "Standard": {
        "icon": "🏨",
        "desc": "Mid-range hotels, local dining, comfort"
    },
    "Luxury": {
        "icon": "💎",
        "desc": "5-star hotels, fine dining, premium"
    }
}

with lifestyle_col1:
    if st.button("🎒", key="budget_btn", use_container_width=True):
        st.session_state.selected_lifestyle = "Budget"
    
    selected_class = "selected" if st.session_state.selected_lifestyle == "Budget" else ""
    st.markdown(f"""
    <div class="lifestyle-card {selected_class}">
        <div class="lifestyle-icon">🎒</div>
        <div class="lifestyle-name">Budget</div>
        <div class="lifestyle-desc">Hostels, street food,<br>public transport</div>
    </div>
    """, unsafe_allow_html=True)

with lifestyle_col2:
    if st.button("🏨", key="standard_btn", use_container_width=True):
        st.session_state.selected_lifestyle = "Standard"
    
    selected_class = "selected" if st.session_state.selected_lifestyle == "Standard" else ""
    st.markdown(f"""
    <div class="lifestyle-card {selected_class}">
        <div class="lifestyle-icon">🏨</div>
        <div class="lifestyle-name">Standard</div>
        <div class="lifestyle-desc">Mid-range hotels,<br>local dining, comfort</div>
    </div>
    """, unsafe_allow_html=True)

with lifestyle_col3:
    if st.button("💎", key="luxury_btn", use_container_width=True):
        st.session_state.selected_lifestyle = "Luxury"
    
    selected_class = "selected" if st.session_state.selected_lifestyle == "Luxury" else ""
    st.markdown(f"""
    <div class="lifestyle-card {selected_class}">
        <div class="lifestyle-icon">💎</div>
        <div class="lifestyle-name">Luxury</div>
        <div class="lifestyle-desc">5-star hotels,<br>fine dining, premium</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; margin-top: 1rem; padding: 0.8rem; background: #f8f9fa; border-radius: 10px;">
    <strong>Selected: {st.session_state.selected_lifestyle}</strong> ✓
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# STEP 4: Calculate
if st.button("🚀 Calculate Smart Budget", type="primary", use_container_width=True):
    
    with st.spinner("🧠 Calculating with AI..."):
        
        # Calculate smart budget with currency conversion
        result = calculate_smart_budget(
            country=country_name,
            lifestyle=st.session_state.selected_lifestyle,
            travelers=travelers,
            days=days,
            currency_code=currency
        )
        
        # Save to session state for dashboard compatibility
        st.session_state.budget_result = {
            "total_cost": result["total_cost"],
            "per_person_cost": result["per_person_cost"],
            "breakdown": result["breakdown"]
        }
        st.session_state.budget_params = {
            "days": days,
            "persons": travelers,
            "currency": currency,
            "country": country_name,
            "lifestyle": st.session_state.selected_lifestyle
        }
        
        # Save to history
        save_budget_history(
            country=country_name,
            travelers=travelers,
            days=days,
            lifestyle=st.session_state.selected_lifestyle,
            total_cost=result["total_cost"],
            currency=currency
        )
        
        st.success("✅ Budget calculated successfully!")
        
        # Display Total Cost
        st.markdown(f"""
        <div class="cost-card">
            <div class="cost-amount">{currency} {result['total_cost']:,.2f}</div>
            <div class="cost-label">Total Trip Cost</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary Stats
        st.markdown("### 📊 Budget Breakdown")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{currency} {result['per_person_cost']:,.0f}</div>
                <div class="stat-label">Per Person</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{currency} {result['daily_cost']:,.0f}</div>
                <div class="stat-label">Per Day</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{days}</div>
                <div class="stat-label">Days</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col4:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{travelers}</div>
                <div class="stat-label">Travelers</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualization and Breakdown
        viz_col1, viz_col2 = st.columns([1.2, 1])
        
        with viz_col1:
            st.markdown("#### 📈 Cost Distribution")
            
            # Plotly Pie Chart
            breakdown = result['breakdown']
            percentages = get_breakdown_percentage(breakdown, result['total_cost'])
            
            fig = go.Figure(data=[go.Pie(
                labels=list(breakdown.keys()),
                values=list(breakdown.values()),
                hole=0.4,
                marker=dict(
                    colors=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'],
                    line=dict(color='white', width=2)
                ),
                textinfo='label+percent',
                textfont=dict(size=14, color='white', family='Inter'),
                hovertemplate='<b>%{label}</b><br>%{value:,.2f} ' + currency + '<br>%{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                showlegend=True,
                height=400,
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    font=dict(size=12, family='Inter')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with viz_col2:
            st.markdown("#### 💳 Expense Details")
            
            breakdown_data = []
            for category, amount in breakdown.items():
                breakdown_data.append({
                    "Category": category,
                    "Amount": f"{currency} {amount:,.2f}",
                    "Share": f"{percentages[category]:.1f}%",
                    "Daily": f"{currency} {amount/days:,.0f}"
                })
            
            df = pd.DataFrame(breakdown_data)
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=350
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # AI Suggestions
        suggestions = generate_smart_suggestions(
            total_cost=result["total_cost"],
            lifestyle=st.session_state.selected_lifestyle,
            travelers=travelers,
            days=days,
            country_category=result["country_category"]
        )
        
        st.markdown("### 🤖 AI-Powered Suggestions")
        
        for suggestion in suggestions:
            color_map = {
                "success": "#10b981",
                "info": "#3b82f6",
                "warning": "#f59e0b"
            }
            border_color = color_map.get(suggestion['type'], "#3b82f6")
            
            st.markdown(f"""
            <div class="suggestion-card" style="border-left-color: {border_color};">
                <div class="suggestion-icon">{suggestion['icon']}</div>
                <div class="suggestion-text">{suggestion['message']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Daily Cost Details
        with st.expander("📋 View Daily Cost Breakdown"):
            daily_costs = result['daily_costs']
            
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.markdown(f"""
                <div class="info-card">
                    <strong>Accommodation</strong><br>
                    {currency} {daily_costs['hotel']:,.2f} per night<br>
                    <small style="color: #666;">Total: {currency} {breakdown['Accommodation']:,.2f}</small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="info-card">
                    <strong>Food & Dining</strong><br>
                    {currency} {daily_costs['food']:,.2f} per day<br>
                    <small style="color: #666;">Total: {currency} {breakdown['Food & Dining']:,.2f}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with detail_col2:
                st.markdown(f"""
                <div class="info-card">
                    <strong>Transportation</strong><br>
                    {currency} {daily_costs['transport']:,.2f} per day<br>
                    <small style="color: #666;">Total: {currency} {breakdown['Transportation']:,.2f}</small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="info-card">
                    <strong>Activities & Tours</strong><br>
                    {currency} {daily_costs['activities']:,.2f} per day<br>
                    <small style="color: #666;">Total: {currency} {breakdown['Activities']:,.2f}</small>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Professional Tips
with st.expander("💡 Professional Travel Budget Tips"):
    tip_col1, tip_col2, tip_col3 = st.columns(3)
    
    with tip_col1:
        st.markdown("""
        **💰 Money Saving**
        - Book 3-6 months in advance
        - Travel during shoulder season
        - Use price comparison tools
        - Set up fare alerts
        - Consider package deals
        """)
    
    with tip_col2:
        st.markdown("""
        **🎯 Smart Planning**
        - Research visa requirements
        - Check local holidays
        - Get travel insurance
        - Keep digital copies of documents
        - Learn basic local phrases
        """)
    
    with tip_col3:
        st.markdown("""
        **🛡️ Safety & Security**
        - Notify your bank
        - Have emergency contacts
        - Keep 15-20% buffer
        - Use secure payment methods
        - Register with embassy
        """)