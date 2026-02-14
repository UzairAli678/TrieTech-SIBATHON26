"""
Dashboard Page
Visualize budget and spending with charts
"""

import streamlit as st
from utils.charts import create_budget_pie_chart, create_daily_vs_total_chart

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

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

st.title("📊 Budget Analytics Dashboard")
st.markdown("Visualize your travel budget with interactive charts")
st.markdown("---")

# Check if budget data exists in session state
if "budget_result" not in st.session_state:
    st.warning("⚠️ No budget data found!")
    st.info("👈 Please go to **Budget Calculator** page and calculate your trip budget first.")
    
    # Show sample data option
    if st.button("📊 View Sample Dashboard"):
        st.session_state.budget_result = {
            "total_cost": 4500.0,
            "per_person_cost": 2250.0,
            "breakdown": {
                "Accommodation": 1400.0,
                "Food & Dining": 1200.0,
                "Transportation": 700.0,
                "Activities": 900.0,
                "Miscellaneous": 300.0
            }
        }
        st.session_state.budget_params = {
            "days": 7,
            "persons": 2,
            "currency": "USD",
            "country": "Sample Country",
            "lifestyle": "Standard"
        }
        st.rerun()
    st.stop()

# Get budget data
result = st.session_state.budget_result
params = st.session_state.get("budget_params", {"days": 7, "persons": 2, "currency": "USD"})

breakdown = result["breakdown"]
total_cost = result["total_cost"]
per_person_cost = result["per_person_cost"]
days = params["days"]
persons = params["persons"]
currency = params["currency"]

# Summary Cards
st.header("💰 Budget Summary")

# Display country and lifestyle if available
if params.get("country") or params.get("lifestyle"):
    info_parts = []
    if params.get("country"):
        info_parts.append(f"📍 **Destination:** {params['country']}")
    if params.get("lifestyle"):
        info_parts.append(f"✨ **Travel Style:** {params['lifestyle']}")
    
    st.markdown(" | ".join(info_parts))
    st.markdown("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Cost",
        value=f"{currency} {total_cost:,.2f}",
        delta=None
    )

with col2:
    st.metric(
        label="Per Person",
        value=f"{currency} {per_person_cost:,.2f}",
        delta=None
    )

with col3:
    daily_cost = total_cost / days
    st.metric(
        label="Daily Cost",
        value=f"{currency} {daily_cost:,.2f}",
        delta=None
    )

with col4:
    highest_category = max(breakdown, key=breakdown.get)
    st.metric(
        label="Highest Expense",
        value=highest_category,
        delta=f"{currency} {breakdown[highest_category]:,.2f}"
    )

st.markdown("---")

# Charts Section
st.header("📊 Visual Analytics")

# Create two columns for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Cost Breakdown")
    pie_fig = create_budget_pie_chart(breakdown, currency)
    st.plotly_chart(pie_fig, use_container_width=True)

with chart_col2:
    st.subheader("Daily vs Total Comparison")
    bar_fig = create_daily_vs_total_chart(breakdown, days, currency)
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")

# Detailed Breakdown Table
st.header("📋 Detailed Breakdown")

import pandas as pd

breakdown_data = []
for category, amount in breakdown.items():
    percentage = (amount / total_cost * 100) if total_cost > 0 else 0
    daily = amount / days
    per_person = amount / persons
    
    breakdown_data.append({
        "Category": category,
        "Total": f"{currency} {amount:,.2f}",
        "Daily": f"{currency} {daily:,.2f}",
        "Per Person": f"{currency} {per_person:,.2f}",
        "Percentage": f"{percentage:.1f}%"
    })

df = pd.DataFrame(breakdown_data)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# Insights Section
st.header("💡 Budget Insights")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("### 📌 Key Observations")
    
    # Find highest and lowest expenses
    sorted_breakdown = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
    
    st.markdown(f"""
    - **Highest expense**: {sorted_breakdown[0][0]} ({currency} {sorted_breakdown[0][1]:,.2f})
    - **Lowest expense**: {sorted_breakdown[-1][0]} ({currency} {sorted_breakdown[-1][1]:,.2f})
    - **Average per category**: {currency} {total_cost/len(breakdown):,.2f}
    - **Daily budget per person**: {currency} {daily_cost/persons:,.2f}
    """)

with col_insight2:
    st.markdown("### ✅ Recommendations")
    
    # Generate smart recommendations - handle both old and new breakdown formats
    # Old format: "Hotel", "Food", "Transport"
    # New format: "Accommodation", "Food & Dining", "Transportation"
    
    hotel_cost = breakdown.get("Accommodation", breakdown.get("Hotel", 0))
    food_cost = breakdown.get("Food & Dining", breakdown.get("Food", 0))
    transport_cost = breakdown.get("Transportation", breakdown.get("Transport", 0))
    
    hotel_pct = (hotel_cost / total_cost * 100) if total_cost > 0 else 0
    food_pct = (food_cost / total_cost * 100) if total_cost > 0 else 0
    
    recommendations = []
    
    if hotel_pct > 40:
        recommendations.append("Consider alternative accommodation to reduce costs")
    
    if food_pct > 40:
        recommendations.append("Look for local markets and budget-friendly restaurants")
    
    if daily_cost > 200:
        recommendations.append("Daily cost is high - consider off-peak travel dates")
    
    if total_cost > 5000:
        recommendations.append("High budget trip - consider travel insurance and payment protection")
    
    if not recommendations:
        recommendations = [
            "Budget looks balanced!",
            "Add 10-15% buffer for emergencies",
            "Book in advance for better rates"
        ]
    
    for rec in recommendations:
        st.markdown(f"- {rec}")

st.markdown("---")

# Action Buttons
col_action1, col_action2 = st.columns(2)

with col_action1:
    if st.button("🔄 Recalculate Budget", type="primary", use_container_width=True):
        st.switch_page("pages/2_💰_Budget_Calculator.py")

with col_action2:
    if st.button("📥 Export Report", use_container_width=True):
        export_data = {
            "Budget Summary": {
                "Total Cost": f"{currency} {total_cost:,.2f}",
                "Per Person": f"{currency} {per_person_cost:,.2f}",
                "Daily Cost": f"{currency} {daily_cost:,.2f}",
                "Days": days,
                "Persons": persons
            },
            "Breakdown": {k: f"{currency} {v:,.2f}" for k, v in breakdown.items()}
        }
        st.json(export_data)
        st.success("✅ Budget report exported!")