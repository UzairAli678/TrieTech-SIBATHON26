"""
Budget calculation utilities
Handles trip budget planning and calculations
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


def calculate_daily_budget(total_budget: float, num_days: int) -> float:
    """
    Calculate daily budget from total budget
    
    Args:
        total_budget: Total trip budget
        num_days: Number of days
        
    Returns:
        Daily budget amount
    """
    if num_days <= 0:
        return 0.0
    return total_budget / num_days


def calculate_per_person_budget(total_budget: float, num_travelers: int) -> float:
    """
    Calculate per person budget
    
    Args:
        total_budget: Total trip budget
        num_travelers: Number of travelers
        
    Returns:
        Per person budget amount
    """
    if num_travelers <= 0:
        return 0.0
    return total_budget / num_travelers


def estimate_trip_cost(
    destination: str,
    num_days: int,
    num_travelers: int,
    travel_style: str = "moderate"
) -> Dict[str, float]:
    """
    Estimate trip cost based on destination and preferences
    
    Args:
        destination: Destination name
        num_days: Number of days
        num_travelers: Number of travelers
        travel_style: Budget style (budget, moderate, luxury)
        
    Returns:
        Dictionary with estimated costs
    """
    # Base daily costs per person by travel style (in USD)
    daily_rates = {
        "budget": {
            "accommodation": 30,
            "food": 20,
            "transport": 10,
            "activities": 15,
            "misc": 10
        },
        "moderate": {
            "accommodation": 80,
            "food": 50,
            "transport": 30,
            "activities": 40,
            "misc": 25
        },
        "luxury": {
            "accommodation": 200,
            "food": 100,
            "transport": 80,
            "activities": 100,
            "misc": 50
        }
    }
    
    rates = daily_rates.get(travel_style, daily_rates["moderate"])
    
    estimates = {}
    for category, daily_cost in rates.items():
        estimates[category] = daily_cost * num_days * num_travelers
    
    estimates["total"] = sum(estimates.values())
    
    return estimates


def get_budget_breakdown(budget_data: Dict[str, float]) -> List[Dict]:
    """
    Get detailed budget breakdown with percentages
    
    Args:
        budget_data: Dictionary of category to amount
        
    Returns:
        List of dictionaries with breakdown details
    """
    total = sum(budget_data.values())
    breakdown = []
    
    for category, amount in budget_data.items():
        percentage = (amount / total * 100) if total > 0 else 0
        breakdown.append({
            "category": category,
            "amount": amount,
            "percentage": percentage,
            "priority": get_category_priority(percentage)
        })
    
    return sorted(breakdown, key=lambda x: x["amount"], reverse=True)


def get_category_priority(percentage: float) -> str:
    """
    Determine priority level based on budget percentage
    
    Args:
        percentage: Budget percentage
        
    Returns:
        Priority level (High, Medium, Low)
    """
    if percentage > 25:
        return "High"
    elif percentage > 10:
        return "Medium"
    else:
        return "Low"


def calculate_emergency_fund(total_budget: float, percentage: float = 15.0) -> float:
    """
    Calculate recommended emergency fund
    
    Args:
        total_budget: Total trip budget
        percentage: Emergency fund percentage (default 15%)
        
    Returns:
        Emergency fund amount
    """
    return total_budget * (percentage / 100)


def optimize_budget(
    budget_data: Dict[str, float],
    target_total: float
) -> Dict[str, float]:
    """
    Optimize budget to meet target total while maintaining proportions
    
    Args:
        budget_data: Current budget allocation
        target_total: Target total budget
        
    Returns:
        Optimized budget allocation
    """
    current_total = sum(budget_data.values())
    
    if current_total == 0:
        return budget_data
    
    scale_factor = target_total / current_total
    
    optimized = {}
    for category, amount in budget_data.items():
        optimized[category] = amount * scale_factor
    
    return optimized


def get_budget_recommendations(destination: str = None) -> Dict[str, float]:
    """
    Get recommended budget allocation percentages
    
    Args:
        destination: Optional destination for specific recommendations
        
    Returns:
        Dictionary of recommended percentages by category
    """
    # General recommendations
    recommendations = {
        "Accommodation": 30.0,
        "Food & Dining": 25.0,
        "Transportation": 20.0,
        "Activities & Tours": 15.0,
        "Emergency Fund": 5.0,
        "Shopping": 3.0,
        "Entertainment": 2.0,
        "Miscellaneous": 0.0
    }
    
    return recommendations


def validate_budget(budget_data: Dict[str, float]) -> List[str]:
    """
    Validate budget and provide warnings
    
    Args:
        budget_data: Budget allocation
        
    Returns:
        List of warning messages
    """
    warnings = []
    total = sum(budget_data.values())
    
    if total == 0:
        warnings.append("Total budget is zero. Please add budget items.")
        return warnings
    
    # Check emergency fund
    emergency = budget_data.get("Emergency Fund", 0)
    if emergency / total < 0.05:
        warnings.append("Emergency fund is less than 5% of total budget.")
    
    # Check accommodation
    accommodation = budget_data.get("Accommodation", 0)
    if accommodation / total > 0.50:
        warnings.append("Accommodation is more than 50% of budget. Consider alternatives.")
    
    # Check if any category is too dominant
    for category, amount in budget_data.items():
        if amount / total > 0.60:
            warnings.append(f"{category} is more than 60% of total budget.")
    
    return warnings
