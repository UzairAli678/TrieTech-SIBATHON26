"""
Chart generation utilities
Creates visualizations for budget and financial data
"""

import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import pandas as pd


def create_pie_chart(
    data: Dict[str, float],
    title: str = "Budget Distribution",
    hole_size: float = 0.4
):
    """
    Create a pie chart from budget data
    
    Args:
        data: Dictionary of categories and amounts
        title: Chart title
        hole_size: Size of center hole (0 for regular pie, >0 for donut)
        
    Returns:
        Plotly figure
    """
    # Filter out zero values
    filtered_data = {k: v for k, v in data.items() if v > 0}
    
    if not filtered_data:
        return None
    
    fig = px.pie(
        values=list(filtered_data.values()),
        names=list(filtered_data.keys()),
        title=title,
        hole=hole_size,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: %{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        showlegend=True,
        height=500
    )
    
    return fig


def create_bar_chart(
    data: Dict[str, float],
    title: str = "Budget by Category",
    orientation: str = 'h',
    color_scale: str = 'Blues'
):
    """
    Create a bar chart from budget data
    
    Args:
        data: Dictionary of categories and amounts
        title: Chart title
        orientation: 'h' for horizontal, 'v' for vertical
        color_scale: Color scale name
        
    Returns:
        Plotly figure
    """
    df = pd.DataFrame({
        'Category': list(data.keys()),
        'Amount': list(data.values())
    })
    
    # Filter and sort
    df = df[df['Amount'] > 0].sort_values('Amount', ascending=(orientation == 'h'))
    
    if df.empty:
        return None
    
    if orientation == 'h':
        fig = px.bar(
            df,
            x='Amount',
            y='Category',
            orientation='h',
            title=title,
            color='Amount',
            color_continuous_scale=color_scale,
            text='Amount'
        )
        fig.update_traces(
            texttemplate='$%{text:,.2f}',
            textposition='outside'
        )
    else:
        fig = px.bar(
            df,
            x='Category',
            y='Amount',
            title=title,
            color='Amount',
            color_continuous_scale=color_scale,
            text='Amount'
        )
        fig.update_traces(
            texttemplate='$%{text:,.2f}',
            textposition='outside'
        )
        fig.update_xaxes(tickangle=-45)
    
    fig.update_layout(
        showlegend=False,
        height=500
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
