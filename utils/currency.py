"""
Currency conversion utilities
Handles real-time exchange rates and currency operations
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.exchangerate.host"
API_KEY = os.getenv("EXCHANGERATE_API_KEY", "")  # Your exchangerate.host API key


def get_supported_currencies() -> List[str]:
    """Get list of supported currency codes"""
    currencies = [
        "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD",
        "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "RUB", "INR", "BRL", "ZAR",
        "DKK", "PLN", "TWD", "THB", "MYR", "IDR", "HUF", "CZK", "ILS", "CLP",
        "PHP", "AED", "SAR", "COP", "ARS", "PKR", "BDT", "VND", "EGP", "NGN"
    ]
    return sorted(currencies)


def get_currency_name(code: str) -> str:
    """Get full currency name from code"""
    names = {
        "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen",
        "AUD": "Australian Dollar", "CAD": "Canadian Dollar", "CHF": "Swiss Franc",
        "CNY": "Chinese Yuan", "SEK": "Swedish Krona", "NZD": "New Zealand Dollar",
        "MXN": "Mexican Peso", "SGD": "Singapore Dollar", "HKD": "Hong Kong Dollar",
        "NOK": "Norwegian Krone", "KRW": "South Korean Won", "TRY": "Turkish Lira",
        "RUB": "Russian Ruble", "INR": "Indian Rupee", "BRL": "Brazilian Real",
        "ZAR": "South African Rand", "DKK": "Danish Krone", "PLN": "Polish Zloty",
        "TWD": "Taiwan Dollar", "THB": "Thai Baht", "MYR": "Malaysian Ringgit",
        "IDR": "Indonesian Rupiah", "HUF": "Hungarian Forint", "CZK": "Czech Koruna",
        "ILS": "Israeli Shekel", "CLP": "Chilean Peso", "PHP": "Philippine Peso",
        "AED": "UAE Dirham", "SAR": "Saudi Riyal", "COP": "Colombian Peso",
        "ARS": "Argentine Peso", "PKR": "Pakistani Rupee", "BDT": "Bangladeshi Taka",
        "VND": "Vietnamese Dong", "EGP": "Egyptian Pound", "NGN": "Nigerian Naira"
    }
    return names.get(code, code)


def convert_currency(amount: float, from_currency: str, to_currency: str) -> Optional[Dict]:
    """
    Convert amount from one currency to another using exchangerate.host API
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
        
    Returns:
        Dictionary with conversion result or None
    """
    try:
        url = f"{API_BASE_URL}/convert"
        params = {
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }
        
        # Add API key if available
        if API_KEY:
            params["access_key"] = API_KEY
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                converted_amount = data.get("result")
                # Calculate rate from result
                rate = converted_amount / amount if amount > 0 else None
                
                return {
                    "converted_amount": converted_amount,
                    "rate": rate,
                    "from": from_currency,
                    "to": to_currency,
                    "date": data.get("date"),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
    except Exception as e:
        print(f"Error converting currency: {e}")
    
    return None
