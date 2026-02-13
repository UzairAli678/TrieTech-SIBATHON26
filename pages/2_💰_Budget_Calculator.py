"""
Budget Calculator Page
Plan and calculate your trip budget
"""

import streamlit as st
import pandas as pd
from utils.budget import calculate_trip_budget, get_breakdown_percentage

st.set_page_config(page_title="Budget Calculator", page_icon="💰", layout="wide")

st.title("💰 Trip Budget Calculator")
st.markdown("Calculate your trip expenses with detailed breakdown")
st.markdown("---")

# Input Section
st.header("📋 Trip Details")

col1, col2 = st.columns(2)

with col1:
    days = st.number_input(
        "Number of Days",
        min_value=1,
        value=7,
        step=1,
        help="Total duration of your trip"
    )
    
    persons = st.number_input(
        "Number of Persons",
        min_value=1,
        value=2,
        step=1,
        help="Total number of travelers"
    )

with col2:
    currency = st.selectbox(
        "Currency",
        ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "INR", "SGD"],
        index=0
    )

st.markdown("---")

# Cost Inputs
st.header("💵 Daily Expenses")

col_a, col_b, col_c = st.columns(3)

with col_a:
    hotel_per_day = st.number_input(
        "Hotel per Day",
        min_value=0.0,
        value=100.0,
        step=10.0,
        format="%.2f",
        help="Total hotel cost per day"
    )

with col_b:
    food_per_day = st.number_input(
        "Food per Person per Day",
        min_value=0.0,
        value=50.0,
        step=5.0,
        format="%.2f",
        help="Food cost per person per day"
    )

with col_c:
    transport_per_day = st.number_input(
        "Transport per Day",
        min_value=0.0,
        value=30.0,
        step=5.0,
        format="%.2f",
        help="Total transport cost per day"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Calculate Button
if st.button("🧮 Calculate Budget", type="primary", use_container_width=True):
    
    result = calculate_trip_budget(
        days=days,
        persons=persons,
        hotel_per_day=hotel_per_day,
        food_per_day=food_per_day,
        transport_per_day=transport_per_day
    )
    
    st.success("✅ Budget calculated successfully!")
    
    # Result Card
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
    
    st.markdown(
        f"<h1 style='color: white; margin: 0;'>{currency} {result['total_cost']:,.2f}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='color: rgba(255,255,255,0.9); font-size: 18px;'>Total Trip Cost</p>",
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Metrics
    st.markdown("### 📊 Summary")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric(
            label="Total Cost",
            value=f"{currency} {result['total_cost']:,.2f}"
        )
    
    with metric_col2:
        st.metric(
            label="Per Person Cost",
            value=f"{currency} {result['per_person_cost']:,.2f}"
        )
    
    with metric_col3:
        daily_cost = result['total_cost'] / days
        st.metric(
            label="Daily Cost",
            value=f"{currency} {daily_cost:,.2f}"
        )
    
    st.markdown("---")
    
    # Breakdown Table
    st.subheader("💳 Cost Breakdown")
    
    breakdown = result['breakdown']
    percentages = get_breakdown_percentage(breakdown, result['total_cost'])
    
    breakdown_data = []
    for category in breakdown.keys():
        breakdown_data.append({
            "Category": category,
            "Amount": f"{currency} {breakdown[category]:,.2f}",
            "Percentage": f"{percentages[category]:.1f}%",
            "Per Day": f"{currency} {breakdown[category]/days:,.2f}",
            "Per Person": f"{currency} {breakdown[category]/persons:,.2f}"
        })
    
    df = pd.DataFrame(breakdown_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Additional Info
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.info(f"""
        **Trip Summary:**
        - Duration: {days} days
        - Travelers: {persons} person(s)
        - Daily budget per person: {currency} {daily_cost/persons:,.2f}
        """)
    
    with col_info2:
        st.warning(f"""
        **Recommendations:**
        - Add 15-20% buffer for emergencies
        - Emergency fund: ~{currency} {result['total_cost']*0.15:,.2f}
        - Total with buffer: ~{currency} {result['total_cost']*1.15:,.2f}
        """)

st.markdown("---")

# Tips Section
with st.expander("💡 Budget Planning Tips"):
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("""
        **Before You Travel:**
        - Research average costs for your destination
        - Book flights and hotels in advance
        - Check for travel deals and discounts
        - Set up travel alerts for price drops
        """)
    
    with col_t2:
        st.markdown("""
        **Money Saving Tips:**
        - Travel during off-peak seasons
        - Use public transportation
        - Eat at local restaurants
        - Look for free attractions and activities
        """)