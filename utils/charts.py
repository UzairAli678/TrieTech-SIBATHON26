"""
Chart generation utilities
Creates visualizations for budget and financial data
"""

import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import pandas as pd


def create_budget_pie_chart(breakdown: Dict[str, float], currency: str = "USD") -> go.Figure:
    """
    Create pie chart for budget breakdown
    
    Args:
        breakdown: Dictionary with Hotel, Food, Transport amounts
        currency: Currency symbol
        
    Returns:
        Plotly figure
    """
    labels = list(breakdown.keys())
    values = list(breakdown.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=['#667eea', '#764ba2', '#f093fb']),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Amount: ' + currency + ' %{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': 'Cost Breakdown by Category',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#333'}
        },
        showlegend=True,
        height=500,
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    return fig


def create_daily_vs_total_chart(
    breakdown: Dict[str, float],
    days: int,
    currency: str = "USD"
) -> go.Figure:
    """
    Create bar chart comparing daily vs total costs
    
    Args:
        breakdown: Dictionary with Hotel, Food, Transport amounts
        days: Number of days
        currency: Currency symbol
        
    Returns:
        Plotly figure
    """
    categories = list(breakdown.keys())
    total_costs = list(breakdown.values())
    daily_costs = [cost / days for cost in total_costs]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Daily Cost',
        x=categories,
        y=daily_costs,
        marker_color='#667eea',
        text=[f'{currency} {val:,.2f}' for val in daily_costs],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Daily: ' + currency + ' %{y:,.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Total Cost',
        x=categories,
        y=total_costs,
        marker_color='#764ba2',
        text=[f'{currency} {val:,.2f}' for val in total_costs],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Total: ' + currency + ' %{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': 'Daily vs Total Cost Comparison',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#333'}
        },
        xaxis_title='Category',
        yaxis_title=f'Amount ({currency})',
        barmode='group',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=100, b=60, l=60, r=40),
        hovermode='x unified'
    )
    
    return fig


def create_line_chart(
    data: List[Dict],
    x_field: str,
    y_field: str,
    title: str = "Trend Over Time",
    color_field: str = None
):
    """
    Create a line chart
    
    Args:
        data: List of data dictionaries
        x_field: Field name for x-axis
        y_field: Field name for y-axis
        title: Chart title
        color_field: Optional field for color grouping
        
    Returns:
        Plotly figure
    """
    df = pd.DataFrame(data)
    
    if df.empty:
        return None
    
    if color_field:
        fig = px.line(
            df,
            x=x_field,
            y=y_field,
            color=color_field,
            title=title,
            markers=True
        )
    else:
        fig = px.line(
            df,
            x=x_field,
            y=y_field,
            title=title,
            markers=True
        )
    
    fig.update_layout(
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_comparison_chart(
    actual_data: Dict[str, float],
    recommended_data: Dict[str, float],
    title: str = "Actual vs Recommended Budget"
):
    """
    Create a grouped bar chart comparing actual vs recommended budget
    
    Args:
        actual_data: Dictionary of actual budget
        recommended_data: Dictionary of recommended percentages
        title: Chart title
        
    Returns:
        Plotly figure
    """
    categories = list(actual_data.keys())
    
    # Calculate percentages for actual data
    total = sum(actual_data.values())
    actual_pct = [(actual_data[cat] / total * 100) if total > 0 else 0 for cat in categories]
    recommended_pct = [recommended_data.get(cat, 0) for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Your Budget',
        x=categories,
        y=actual_pct,
        marker_color='rgb(55, 83, 109)',
        text=[f"{val:.1f}%" for val in actual_pct],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='Recommended',
        x=categories,
        y=recommended_pct,
        marker_color='rgb(26, 118, 255)',
        text=[f"{val:.1f}%" for val in recommended_pct],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Category',
        yaxis_title='Percentage (%)',
        barmode='group',
        height=500,
        xaxis_tickangle=-45
    )
    
    return fig


def create_gauge_chart(
    value: float,
    max_value: float,
    title: str = "Budget Usage",
    thresholds: Dict[str, List[float]] = None
):
    """
    Create a gauge chart for budget tracking
    
    Args:
        value: Current value
        max_value: Maximum value
        title: Chart title
        thresholds: Dictionary with 'values' and 'colors' keys
        
    Returns:
        Plotly figure
    """
    if thresholds is None:
        thresholds = {
            'values': [max_value * 0.6, max_value * 0.8, max_value],
            'colors': ['green', 'yellow', 'red']
        }
    
    percentage = (value / max_value * 100) if max_value > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': max_value},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, thresholds['values'][0]], 'color': thresholds['colors'][0]},
                {'range': [thresholds['values'][0], thresholds['values'][1]], 'color': thresholds['colors'][1]},
                {'range': [thresholds['values'][1], thresholds['values'][2]], 'color': thresholds['colors'][2]}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value
            }
        }
    ))
    
    fig.update_layout(height=400)
    
    return fig


def create_sunburst_chart(
    data: Dict[str, float],
    title: str = "Budget Hierarchy"
):
    """
    Create a sunburst chart for hierarchical budget data
    
    Args:
        data: Dictionary of categories and amounts
        title: Chart title
        
    Returns:
        Plotly figure
    """
    # Prepare data for sunburst
    labels = ["Total"] + list(data.keys())
    parents = [""] + ["Total"] * len(data)
    values = [sum(data.values())] + list(data.values())
    
    fig = px.sunburst(
        names=labels,
        parents=parents,
        values=values,
        title=title
    )
    
    fig.update_layout(height=500)
    
    return fig
