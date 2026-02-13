"""
Budget Calculator Page
Plan and calculate your trip budget
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.budget import calculate_daily_budget, estimate_trip_cost, get_budget_breakdown
from config.settings import DEFAULT_BUDGET_CATEGORIES

st.set_page_config(page_title="Budget Calculator", page_icon="💰", layout="wide")

st.title("💰 Trip Budget Calculator")
st.markdown("Plan your trip expenses and stay within budget")

# Initialize session state
if "budget_data" not in st.session_state:
    st.session_state.budget_data = {cat: 0.0 for cat in DEFAULT_BUDGET_CATEGORIES}

# Trip Information
st.header("🗓️ Trip Details")

col1, col2, col3 = st.columns(3)

with col1:
    destination = st.text_input("Destination", placeholder="e.g., Paris, France")

with col2:
    start_date = st.date_input("Start Date", value=datetime.now())

with col3:
    end_date = st.date_input("End Date", value=datetime.now() + timedelta(days=7))

col4, col5 = st.columns(2)

with col4:
    num_travelers = st.number_input("Number of Travelers", min_value=1, value=1, step=1)

with col5:
    currency = st.selectbox("Budget Currency", ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "INR"])

# Calculate trip duration
if end_date >= start_date:
    trip_duration = (end_date - start_date).days + 1
    st.info(f"Trip Duration: **{trip_duration} days** | Travelers: **{num_travelers}**")
else:
    st.error("End date must be after start date!")
    trip_duration = 0

st.markdown("---")

# Budget Categories
st.header("💵 Budget Breakdown")

st.markdown("### Enter your estimated expenses for each category:")

# Create two columns for budget input
col_left, col_right = st.columns(2)

categories_left = DEFAULT_BUDGET_CATEGORIES[:4]
categories_right = DEFAULT_BUDGET_CATEGORIES[4:]

with col_left:
    for category in categories_left:
        st.session_state.budget_data[category] = st.number_input(
            f"{category}",
            min_value=0.0,
            value=st.session_state.budget_data.get(category, 0.0),
            step=50.0,
            key=f"budget_{category}"
        )

with col_right:
    for category in categories_right:
        st.session_state.budget_data[category] = st.number_input(
            f"{category}",
            min_value=0.0,
            value=st.session_state.budget_data.get(category, 0.0),
            step=50.0,
            key=f"budget_{category}"
        )

# Calculate totals
total_budget = sum(st.session_state.budget_data.values())
total_per_person = total_budget / num_travelers if num_travelers > 0 else 0
daily_budget = total_budget / trip_duration if trip_duration > 0 else 0

st.markdown("---")

# Budget Summary
st.header("📊 Budget Summary")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Total Budget", f"{currency} {total_budget:,.2f}")

with metric_col2:
    st.metric("Per Person", f"{currency} {total_per_person:,.2f}")

with metric_col3:
    st.metric("Daily Budget", f"{currency} {daily_budget:,.2f}")

with metric_col4:
    st.metric("Per Person/Day", f"{currency} {daily_budget/num_travelers if num_travelers > 0 else 0:,.2f}")

# Budget breakdown table
st.subheader("Category Breakdown")

breakdown_data = []
for category, amount in st.session_state.budget_data.items():
    if total_budget > 0:
        percentage = (amount / total_budget) * 100
    else:
        percentage = 0
    
    breakdown_data.append({
        "Category": category,
        "Amount": f"{currency} {amount:,.2f}",
        "Percentage": f"{percentage:.1f}%",
        "Daily": f"{currency} {amount/trip_duration if trip_duration > 0 else 0:,.2f}"
    })

df_breakdown = pd.DataFrame(breakdown_data)
st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

st.markdown("---")

# Tips and Recommendations
st.header("💡 Budget Tips")

col_tip1, col_tip2 = st.columns(2)

with col_tip1:
    st.markdown("""
    ### 🎯 Smart Budgeting
    - Add 15-20% buffer for emergencies
    - Research average costs for your destination
    - Book accommodation and flights in advance
    - Use public transportation when possible
    """)

with col_tip2:
    st.markdown("""
    ### 💳 Money-Saving Tips
    - Compare prices across multiple platforms
    - Look for free attractions and activities
    - Eat at local restaurants
    - Travel during off-peak seasons
    """)

# Export budget
st.markdown("---")
if st.button("📥 Export Budget Plan", type="primary"):
    export_data = {
        "Trip Information": {
            "Destination": destination,
            "Start Date": start_date.strftime("%Y-%m-%d"),
            "End Date": end_date.strftime("%Y-%m-%d"),
            "Duration": f"{trip_duration} days",
            "Travelers": num_travelers,
            "Currency": currency
        },
        "Budget Summary": {
            "Total": total_budget,
            "Per Person": total_per_person,
            "Daily": daily_budget
        },
        "Categories": st.session_state.budget_data
    }
    
    st.json(export_data)
    st.success("✅ Budget plan ready! You can copy the JSON above.")
