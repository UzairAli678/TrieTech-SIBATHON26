"""
AI Assistant utilities
Handles chatbot functionality and AI responses
"""

import os
from typing import List, Dict
from config.settings import AI_MODEL, AI_TEMPERATURE, AI_MAX_TOKENS, OPENAI_API_KEY


def initialize_conversation() -> List[Dict]:
    """
    Initialize conversation with system prompt
    
    Returns:
        List with system message
    """
    system_message = {
        "role": "system",
        "content": """You are a helpful travel planning assistant. You provide advice on:
        - Travel destinations and recommendations
        - Budget planning and money-saving tips
        - Best times to visit locations
        - Local customs, culture, and etiquette
        - Packing tips and travel essentials
        - Safety and health advice
        - Transportation and accommodation suggestions
        - Food and dining recommendations
        
        Keep responses concise, practical, and friendly. Provide specific examples when possible.
        If you don't know something, admit it and suggest reliable resources."""
    }
    
    return [system_message]


def get_ai_response(user_message: str, chat_history: List[Dict]) -> str:
    """
    Get AI response to user message
    
    Args:
        user_message: User's message
        chat_history: Previous conversation history
        
    Returns:
        AI response text
    """
    # Check if OpenAI API key is available
    if not OPENAI_API_KEY or OPENAI_API_KEY == "":
        return get_fallback_response(user_message)
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Prepare messages for API
        messages = initialize_conversation()
        
        # Add relevant history (last 10 messages to stay within token limits)
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        
        for msg in recent_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
            temperature=AI_TEMPERATURE,
            max_tokens=AI_MAX_TOKENS
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return get_fallback_response(user_message)


def get_fallback_response(user_message: str) -> str:
    """
    Provide fallback responses when AI is unavailable
    
    Args:
        user_message: User's message
        
    Returns:
        Fallback response
    """
    user_message_lower = user_message.lower()
    
    # Budget-related questions
    if any(word in user_message_lower for word in ["budget", "cost", "expensive", "cheap", "price"]):
        return """💰 **Budget Travel Tips:**

- Research average costs for your destination in advance
- Book flights and accommodation 2-3 months ahead
- Travel during off-peak seasons (20-40% savings)
- Use public transportation instead of taxis
- Eat at local restaurants away from tourist areas
- Look for free walking tours and attractions
- Consider hostels or Airbnb for accommodation
- Set a daily spending limit and track expenses

Would you like specific budget estimates for a particular destination?"""
    
    # Destination recommendations
    elif any(word in user_message_lower for word in ["where", "recommend", "destination", "visit", "travel to"]):
        return """🌍 **Popular Travel Destinations by Interest:**

**Culture & History:**
- Rome, Italy - Ancient ruins and Renaissance art
- Kyoto, Japan - Traditional temples and gardens
- Cairo, Egypt - Pyramids and ancient wonders

**Nature & Adventure:**
- New Zealand - Hiking, mountains, scenic beauty
- Costa Rica - Rainforests and wildlife
- Iceland - Volcanoes, waterfalls, northern lights

**Beach & Relaxation:**
- Maldives - Luxury resorts and crystal waters
- Bali, Indonesia - Beaches, culture, affordable
- Greek Islands - Beautiful scenery and history

What type of experience are you looking for?"""
    
    # Packing tips
    elif any(word in user_message_lower for word in ["pack", "luggage", "bring", "carry"]):
        return """🎒 **Smart Packing Tips:**

**Essentials:**
- Passport, visas, copies of important documents
- Credit cards and some local currency
- Travel insurance documents
- Necessary medications
- Universal power adapter
- Phone charger and power bank

**Clothing Tips:**
- Mix-and-match versatile pieces
- Layer for different weather
- 1-2 pairs of comfortable shoes
- Quick-dry fabrics
- One dressy outfit

**Space Savers:**
- Roll clothes instead of folding
- Use packing cubes
- Wear bulkiest items on travel day
- Bring travel-size toiletries

Check weather forecast before finalizing your packing list!"""
    
    # Safety tips
    elif any(word in user_message_lower for word in ["safe", "safety", "danger", "security"]):
        return """🛡️ **Travel Safety Tips:**

**Before You Go:**
- Research your destination's safety situation
- Register with your embassy
- Get travel insurance
- Make copies of important documents

**While Traveling:**
- Stay aware of your surroundings
- Don't display expensive items
- Use hotel safes for valuables
- Keep emergency contacts handy
- Avoid walking alone at night in unfamiliar areas
- Trust your instincts

**Money Safety:**
- Use ATMs in secure locations
- Don't carry all cash in one place
- Notify your bank of travel plans
- Use credit cards when possible

Stay safe and enjoy your trip!"""
    
    # Best time to visit
    elif any(word in user_message_lower for word in ["when", "time", "season", "weather"]):
        return """📅 **Choosing the Best Travel Time:**

**Consider These Factors:**

**Weather:**
- Check seasonal climate patterns
- Avoid extreme temperatures or monsoon seasons
- Consider your weather preferences

**Crowds:**
- Peak season = More crowds, higher prices
- Shoulder season = Better balance
- Off-season = Cheaper but some closures

**Events:**
- Festivals and local celebrations
- Holidays (may affect prices/availability)
- Special events you want to attend

**Budget:**
- Off-peak = 20-40% savings
- Book flights on Tuesdays/Wednesdays
- Travel mid-week when possible

Which destination are you interested in?"""
    
    # Food and dining
    elif any(word in user_message_lower for word in ["food", "eat", "restaurant", "cuisine"]):
        return """🍽️ **Food & Dining Travel Tips:**

**Eating Smart:**
- Try local street food (usually authentic and cheap)
- Ask locals for restaurant recommendations
- Eat where locals eat, not tourist traps
- Learn basic food phrases in local language
- Be adventurous but know your limits

**Budget Tips:**
- Lunch menus often cheaper than dinner
- Markets for fresh, affordable food
- Stay in places with kitchen facilities
- Carry snacks for cheaper options

**Food Safety:**
- Choose busy restaurants (high turnover)
- Drink bottled water if advised
- Be careful with raw foods in some regions
- Keep hand sanitizer handy

**Cultural Etiquette:**
- Research tipping customs
- Learn basic dining manners
- Respect dietary restrictions/customs

Happy eating! 🌮🍜🍕"""
    
    # Default response
    else:
        return """🤖 **I'm here to help with your travel planning!**

I can assist you with:

✈️ **Destination Recommendations** - Where to go based on your interests
💰 **Budget Planning** - How to plan and save money
🎒 **Packing Tips** - What to bring for your trip
📅 **Best Times to Visit** - When to travel to avoid crowds
🛡️ **Safety Advice** - How to stay safe abroad
🍽️ **Food & Dining** - Where and what to eat
🗺️ **Itinerary Planning** - How to organize your trip

**Note:** For this demo, I'm providing general advice. For personalized AI responses, please add your OpenAI API key to the .env file.

What aspect of travel planning can I help you with?"""


def analyze_budget_input(budget_data: Dict) -> str:
    """
    Analyze budget data and provide recommendations
    
    Args:
        budget_data: Dictionary with budget categories and amounts
        
    Returns:
        Analysis and recommendations
    """
    total = sum(budget_data.values())
    
    if total == 0:
        return "No budget data to analyze. Please create a budget first."
    
    # Calculate percentages
    percentages = {k: (v / total * 100) for k, v in budget_data.items() if v > 0}
    
    # Find top categories
    top_categories = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:3]
    
    analysis = f"""📊 **Budget Analysis:**

**Total Budget:** ${total:,.2f}

**Top Expenses:**
"""
    
    for i, (category, pct) in enumerate(top_categories, 1):
        amount = budget_data[category]
        analysis += f"{i}. {category}: ${amount:,.2f} ({pct:.1f}%)\n"
    
    # Recommendations
    analysis += "\n**Recommendations:**\n"
    
    if percentages.get("Emergency Fund", 0) < 5:
        analysis += "- Consider adding 10-15% for emergency fund\n"
    
    if percentages.get("Accommodation", 0) > 40:
        analysis += "- Accommodation seems high, consider alternatives like hostels or Airbnb\n"
    
    if percentages.get("Food & Dining", 0) < 15:
        analysis += "- Food budget might be low, ensure adequate allocation\n"
    
    return analysis
