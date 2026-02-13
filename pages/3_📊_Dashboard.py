"""
Dashboard Page
Visualize budget and spending with charts
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.settings import DEFAULT_BUDGET_CATEGORIES
from utils.charts import create_pie_chart, create_bar_chart, create_line_chart

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Budget Analytics Dashboard")
st.markdown("Visualize your travel budget and spending patterns")

# Check if budget data exists
if "budget_data" not in st.session_state or sum(st.session_state.budget_data.values()) == 0:
    st.warning("⚠️ No budget data found. Please create a budget in the Budget Calculator page first!")
    st.info("👈 Navigate to **Budget Calculator** to set up your trip budget.")
    st.stop()

budget_data = st.session_state.budget_data
total_budget = sum(budget_data.values())

# Key Metrics
st.header("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Budget", f"${total_budget:,.2f}", delta="100%")

with col2:
    largest_category = max(budget_data, key=budget_data.get)
    st.metric("Largest Category", largest_category, delta=f"${budget_data[largest_category]:,.2f}")

with col3:
    num_categories = sum(1 for v in budget_data.values() if v > 0)
    st.metric("Active Categories", num_categories, delta=f"of {len(budget_data)}")

with col4:
    avg_category = total_budget / num_categories if num_categories > 0 else 0
    st.metric("Avg per Category", f"${avg_category:,.2f}")

st.markdown("---")

# Charts
st.header("📊 Budget Visualization")

tab1, tab2, tab3 = st.tabs(["Pie Chart", "Bar Chart", "Comparison"])

with tab1:
    st.subheader("Budget Distribution")
    
    # Filter out zero values for cleaner visualization
    filtered_data = {k: v for k, v in budget_data.items() if v > 0}
    
    if filtered_data:
        fig_pie = px.pie(
            values=list(filtered_data.values()),
            names=list(filtered_data.keys()),
            title="Budget Allocation by Category",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=500)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No budget data to display")

with tab2:
    st.subheader("Category Comparison")
    
    df_budget = pd.DataFrame({
        'Category': list(budget_data.keys()),
        'Amount': list(budget_data.values())
    })
    df_budget = df_budget[df_budget['Amount'] > 0].sort_values('Amount', ascending=True)
    
    if not df_budget.empty:
        fig_bar = px.bar(
            df_budget,
            x='Amount',
            y='Category',
            orientation='h',
            title="Budget by Category",
            color='Amount',
            color_continuous_scale='Blues',
            text='Amount'
        )
        fig_bar.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
        fig_bar.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No budget data to display")

with tab3:
    st.subheader("Budget vs Recommended Allocation")
    
    # Recommended budget percentages (example)
    recommended = {
        "Accommodation": 30,
        "Food & Dining": 25,
        "Transportation": 20,
        "Activities & Tours": 15,
        "Shopping": 5,
        "Entertainment": 3,
        "Emergency Fund": 2,
        "Miscellaneous": 0
    }
    
    comparison_data = []
    for category in DEFAULT_BUDGET_CATEGORIES:
        if budget_data[category] > 0:
            actual_pct = (budget_data[category] / total_budget * 100) if total_budget > 0 else 0
            recommended_pct = recommended.get(category, 0)
            comparison_data.append({
                'Category': category,
                'Your Budget': actual_pct,
                'Recommended': recommended_pct
            })
    
    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            name='Your Budget',
            x=df_comparison['Category'],
            y=df_comparison['Your Budget'],
            marker_color='rgb(55, 83, 109)'
        ))
        fig_comparison.add_trace(go.Bar(
            name='Recommended',
            x=df_comparison['Category'],
            y=df_comparison['Recommended'],
            marker_color='rgb(26, 118, 255)'
        ))
        
        fig_comparison.update_layout(
            title='Your Budget vs Recommended Allocation (%)',
            xaxis_title='Category',
            yaxis_title='Percentage (%)',
            barmode='group',
            height=500
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        st.info("💡 **Tip**: These are general recommendations. Adjust based on your travel style and destination!")

st.markdown("---")

# Detailed breakdown table
st.header("📋 Detailed Breakdown")

detailed_data = []
for category, amount in budget_data.items():
    if amount > 0:
        percentage = (amount / total_budget * 100) if total_budget > 0 else 0
        detailed_data.append({
            "Category": category,
            "Amount ($)": f"{amount:,.2f}",
            "Percentage": f"{percentage:.1f}%",
            "Priority": "High" if percentage > 25 else "Medium" if percentage > 10 else "Low"
        })

df_detailed = pd.DataFrame(detailed_data)
st.dataframe(df_detailed, use_container_width=True, hide_index=True)

# Insights
st.markdown("---")
st.header("💡 Budget Insights")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("### 📌 Observations")
    if budget_data:
        top_3 = sorted(budget_data.items(), key=lambda x: x[1], reverse=True)[:3]
        st.markdown(f"- **Top expense**: {top_3[0][0]} (${top_3[0][1]:,.2f})")
        if len(top_3) > 1:
            st.markdown(f"- **Second**: {top_3[1][0]} (${top_3[1][1]:,.2f})")
        if len(top_3) > 2:
            st.markdown(f"- **Third**: {top_3[2][0]} (${top_3[2][1]:,.2f})")

with col_insight2:
    st.markdown("### ✅ Recommendations")
    st.markdown("""
    - Consider allocating 10-15% for emergencies
    - Book accommodation early for better rates
    - Use budget airlines for cost savings
    - Research free activities at destination
    """)
