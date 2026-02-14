"""
Budget calculation utilities - Professional AI-Powered Trip Budget System
Handles intelligent trip budget planning with real-world cost estimation
"""

from typing import Dict, List, Optional, Tuple
import requests
import json
import os
from datetime import datetime
from utils.currency import convert_currency


# Country Cost Categories based on real-world data
COUNTRY_COST_CATEGORIES = {
    "high": [
        "Switzerland", "Norway", "Iceland", "Denmark", "Luxembourg",
        "United States", "United Kingdom", "Australia", "Singapore",
        "United Arab Emirates", "Japan", "Sweden", "Ireland", "Finland",
        "Netherlands", "Germany", "France", "Belgium", "Austria", "Canada"
    ],
    "medium": [
        "Spain", "Italy", "Portugal", "Greece", "Turkey", "Poland",
        "Czech Republic", "Hungary", "Croatia", "Malaysia", "Thailand",
        "Vietnam", "Philippines", "Indonesia", "Brazil", "Mexico",
        "Argentina", "Chile", "South Africa", "Egypt", "Morocco"
    ],
    "low": [
        "India", "Pakistan", "Bangladesh", "Nepal", "Sri Lanka",
        "Cambodia", "Laos", "Myanmar", "Bolivia", "Peru",
        "Ecuador", "Colombia", "Guatemala", "Honduras", "Nicaragua"
    ]
}

# Lifestyle-based cost multipliers (all prices in USD per day)
LIFESTYLE_COSTS = {
    "Luxury": {
        "hotel": {"high": 450, "medium": 280, "low": 180},
        "food": {"high": 120, "medium": 85, "low": 50},
        "transport": {"high": 80, "medium": 50, "low": 30},
        "activities": {"high": 150, "medium": 100, "low": 60}
    },
    "Standard": {
        "hotel": {"high": 180, "medium": 100, "low": 60},
        "food": {"high": 60, "medium": 40, "low": 25},
        "transport": {"high": 40, "medium": 25, "low": 15},
        "activities": {"high": 60, "medium": 40, "low": 25}
    },
    "Budget": {
        "hotel": {"high": 80, "medium": 45, "low": 25},
        "food": {"high": 35, "medium": 22, "low": 12},
        "transport": {"high": 20, "medium": 12, "low": 8},
        "activities": {"high": 30, "medium": 20, "low": 12}
    }
}


def fetch_countries() -> List[Dict]:
    """
    Fetch countries from REST Countries API
    
    Returns:
        List of country dictionaries with name, currency, and flag
    """
    try:
        response = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            countries = []
            
            for country in data:
                # Extract common name
                name = country.get("name", {}).get("common", "Unknown")
                
                # Extract first currency
                currencies = country.get("currencies", {})
                currency_code = list(currencies.keys())[0] if currencies else "USD"
                currency_name = currencies.get(currency_code, {}).get("name", "Dollar") if currencies else "Dollar"
                
                # Extract flag emoji
                flag = country.get("flag", "🌍")
                
                countries.append({
                    "name": name,
                    "currency": currency_code,
                    "currency_name": currency_name,
                    "flag": flag
                })
            
            # Sort alphabetically
            countries.sort(key=lambda x: x["name"])
            return countries
        else:
            return get_fallback_countries()
            
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return get_fallback_countries()


def get_fallback_countries() -> List[Dict]:
    """Fallback country list if API fails"""
    return [
        {"name": "United States", "currency": "USD", "currency_name": "US Dollar", "flag": "🇺🇸"},
        {"name": "United Kingdom", "currency": "GBP", "currency_name": "British Pound", "flag": "🇬🇧"},
        {"name": "France", "currency": "EUR", "currency_name": "Euro", "flag": "🇫🇷"},
        {"name": "Japan", "currency": "JPY", "currency_name": "Japanese Yen", "flag": "🇯🇵"},
        {"name": "Australia", "currency": "AUD", "currency_name": "Australian Dollar", "flag": "🇦🇺"},
        {"name": "Canada", "currency": "CAD", "currency_name": "Canadian Dollar", "flag": "🇨🇦"},
        {"name": "Switzerland", "currency": "CHF", "currency_name": "Swiss Franc", "flag": "🇨🇭"},
        {"name": "UAE", "currency": "AED", "currency_name": "UAE Dirham", "flag": "🇦🇪"},
        {"name": "Singapore", "currency": "SGD", "currency_name": "Singapore Dollar", "flag": "🇸🇬"},
        {"name": "Thailand", "currency": "THB", "currency_name": "Thai Baht", "flag": "🇹🇭"},
        {"name": "India", "currency": "INR", "currency_name": "Indian Rupee", "flag": "🇮🇳"},
        {"name": "Pakistan", "currency": "PKR", "currency_name": "Pakistani Rupee", "flag": "🇵🇰"},
        {"name": "Turkey", "currency": "TRY", "currency_name": "Turkish Lira", "flag": "🇹🇷"},
        {"name": "Spain", "currency": "EUR", "currency_name": "Euro", "flag": "🇪🇸"},
        {"name": "Italy", "currency": "EUR", "currency_name": "Euro", "flag": "🇮🇹"},
        {"name": "Germany", "currency": "EUR", "currency_name": "Euro", "flag": "🇩🇪"},
        {"name": "Brazil", "currency": "BRL", "currency_name": "Brazilian Real", "flag": "🇧🇷"},
        {"name": "Mexico", "currency": "MXN", "currency_name": "Mexican Peso", "flag": "🇲🇽"},
    ]


def get_country_category(country_name: str) -> str:
    """
    Determine country cost category (high/medium/low)
    
    Args:
        country_name: Name of the country
        
    Returns:
        Category: 'high', 'medium', or 'low'
    """
    for category, countries in COUNTRY_COST_CATEGORIES.items():
        if any(country.lower() in country_name.lower() or country_name.lower() in country.lower() 
               for country in countries):
            return category
    
    # Default to medium if not found
    return "medium"


def calculate_smart_budget(
    country: str,
    lifestyle: str,
    travelers: int,
    days: int,
    currency_code: str = "USD"
) -> Dict:
    """
    Calculate smart budget based on country, lifestyle, travelers, and days
    
    Args:
        country: Country name
        lifestyle: Lifestyle choice (Luxury/Standard/Budget)
        travelers: Number of travelers
        days: Number of days
        currency_code: Target currency code for conversion
        
    Returns:
        Dictionary with detailed budget breakdown in target currency
    """
    # Get country cost category
    category = get_country_category(country)
    
    # Get costs for the lifestyle and category (in USD)
    costs = LIFESTYLE_COSTS[lifestyle]
    
    # Calculate daily costs in USD
    hotel_per_day_usd = costs["hotel"][category]
    food_per_day_usd = costs["food"][category] * travelers  # Food multiplied by travelers
    transport_per_day_usd = costs["transport"][category]
    activities_per_day_usd = costs["activities"][category]
    
    # Calculate totals in USD
    hotel_total_usd = hotel_per_day_usd * days
    food_total_usd = food_per_day_usd * days
    transport_total_usd = transport_per_day_usd * days
    activities_total_usd = activities_per_day_usd * days
    
    # Add miscellaneous (10% of total)
    subtotal_usd = hotel_total_usd + food_total_usd + transport_total_usd + activities_total_usd
    misc_total_usd = subtotal_usd * 0.10
    
    total_cost_usd = subtotal_usd + misc_total_usd
    
    # Convert to target currency if not USD
    exchange_rate = 1.0
    if currency_code != "USD":
        conversion = convert_currency(total_cost_usd, "USD", currency_code)
        if conversion and conversion.get("rate"):
            exchange_rate = conversion["rate"]
    
    # Apply exchange rate to all amounts
    hotel_total = hotel_total_usd * exchange_rate
    food_total = food_total_usd * exchange_rate
    transport_total = transport_total_usd * exchange_rate
    activities_total = activities_total_usd * exchange_rate
    misc_total = misc_total_usd * exchange_rate
    total_cost = total_cost_usd * exchange_rate
    
    per_person_cost = total_cost / travelers if travelers > 0 else 0
    daily_cost = total_cost / days if days > 0 else 0
    
    breakdown = {
        "Accommodation": hotel_total,
        "Food & Dining": food_total,
        "Transportation": transport_total,
        "Activities": activities_total,
        "Miscellaneous": misc_total
    }
    
    return {
        "total_cost": total_cost,
        "per_person_cost": per_person_cost,
        "daily_cost": daily_cost,
        "breakdown": breakdown,
        "country_category": category,
        "currency_code": currency_code,
        "exchange_rate": exchange_rate,
        "daily_costs": {
            "hotel": hotel_per_day_usd * exchange_rate,
            "food": food_per_day_usd * exchange_rate,
            "transport": transport_per_day_usd * exchange_rate,
            "activities": activities_per_day_usd * exchange_rate
        }
    }


def generate_smart_suggestions(
    total_cost: float,
    lifestyle: str,
    travelers: int,
    days: int,
    country_category: str
) -> List[Dict[str, str]]:
    """
    Generate AI-style smart suggestions based on budget parameters
    
    Args:
        total_cost: Total calculated cost
        lifestyle: Selected lifestyle
        travelers: Number of travelers
        days: Number of days
        country_category: Country cost category
        
    Returns:
        List of suggestion dictionaries with 'type' and 'message'
    """
    suggestions = []
    
    # Lifestyle suggestions
    if lifestyle == "Luxury" and total_cost > 5000:
        suggestions.append({
            "type": "info",
            "icon": "💡",
            "message": "Consider switching to Standard lifestyle to reduce costs by ~40%"
        })
    
    if lifestyle == "Budget" and country_category == "high":
        suggestions.append({
            "type": "warning",
            "icon": "⚠️",
            "message": f"Budget travel in high-cost countries can be challenging. Consider medium-cost alternatives."
        })
    
    if lifestyle == "Budget":
        suggestions.append({
            "type": "success",
            "icon": "✨",
            "message": "Great choice! Consider upgrading specific experiences for more comfort."
        })
    
    # Traveler-based suggestions
    if travelers > 4:
        suggestions.append({
            "type": "success",
            "icon": "👥",
            "message": f"Group of {travelers}! You may qualify for group discounts on accommodation and tours."
        })
    
    if travelers == 1:
        suggestions.append({
            "type": "info",
            "icon": "🧳",
            "message": "Solo travel tip: Consider hostels or homestays for social experiences."
        })
    
    # Duration suggestions
    if days > 14:
        suggestions.append({
            "type": "info",
            "icon": "📅",
            "message": "Long trip! Look for monthly rates on accommodation for better deals."
        })
    
    if days < 4:
        suggestions.append({
            "type": "warning",
            "icon": "⏰",
            "message": "Short trip! Focus budget on key experiences rather than accommodation."
        })
    
    # Cost-based suggestions
    per_day_cost = total_cost / days if days > 0 else 0
    
    if per_day_cost < 100:
        suggestions.append({
            "type": "success",
            "icon": "💰",
            "message": "Excellent budget! You're planning an affordable adventure."
        })
    elif per_day_cost > 500:
        suggestions.append({
            "type": "info",
            "icon": "💎",
            "message": "Premium travel experience! Consider travel insurance for peace of mind."
        })
    
    # Country category suggestions
    if country_category == "high":
        suggestions.append({
            "type": "info",
            "icon": "🌍",
            "message": "High-cost destination. Book flights and hotels early for best rates."
        })
    
    # Emergency fund suggestion
    emergency_fund = total_cost * 0.15
    suggestions.append({
        "type": "warning",
        "icon": "🆘",
        "message": f"Add 15% emergency buffer (~${emergency_fund:,.0f}) for unexpected expenses."
    })
    
    return suggestions


def save_budget_history(
    country: str,
    travelers: int,
    days: int,
    lifestyle: str,
    total_cost: float,
    currency: str
) -> bool:
    """
    Save budget calculation to history file
    
    Args:
        country: Country name
        travelers: Number of travelers
        days: Number of days
        lifestyle: Lifestyle category
        total_cost: Total cost
        currency: Currency code
        
    Returns:
        Boolean indicating success
    """
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        history_file = "data/budget_history.json"
        
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        # Add new entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "country": country,
            "travelers": travelers,
            "days": days,
            "lifestyle": lifestyle,
            "total_cost": total_cost,
            "currency": currency
        }
        
        history.append(entry)
        
        # Keep only last 100 entries
        history = history[-100:]
        
        # Save
        with open(history_file, 'w') as f:
            json.dump(history, indent=2, fp=f)
        
        return True
        
    except Exception as e:
        print(f"Error saving budget history: {e}")
        return False


def get_breakdown_percentage(breakdown: Dict[str, float], total: float) -> Dict[str, float]:
    """
    Calculate percentage for each category
    
    Args:
        breakdown: Dictionary with category amounts
        total: Total amount
        
    Returns:
        Dictionary with category percentages
    """
    if total == 0:
        return {k: 0 for k in breakdown.keys()}
    
    return {k: (v / total * 100) for k, v in breakdown.items()}


# Legacy function for backward compatibility
def calculate_trip_budget(
    days: int,
    persons: int,
    hotel_per_day: float,
    food_per_day: float,
    transport_per_day: float
) -> Dict:
    """
    Calculate trip budget with breakdown (Legacy function)
    
    Args:
        days: Number of days
        persons: Number of persons
        hotel_per_day: Hotel cost per day
        food_per_day: Food cost per day per person
        transport_per_day: Transport cost per day
        
    Returns:
        Dictionary with total_cost, per_person_cost, and breakdown
    """
    hotel_total = hotel_per_day * days
    food_total = food_per_day * days * persons
    transport_total = transport_per_day * days
    
    total_cost = hotel_total + food_total + transport_total
    per_person_cost = total_cost / persons if persons > 0 else 0
    
    breakdown = {
        "Hotel": hotel_total,
        "Food": food_total,
        "Transport": transport_total
    }
    
    return {
        "total_cost": total_cost,
        "per_person_cost": per_person_cost,
        "breakdown": breakdown
    }
