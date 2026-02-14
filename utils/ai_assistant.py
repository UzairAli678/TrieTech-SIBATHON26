"""
AI Assistant utilities - Groq API Integration
Handles chatbot functionality and AI responses for tourist assistance
Uses Groq's ultra-fast LLM API with Llama models
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Get Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Initialize Groq client
client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)


def get_system_prompt(country: Optional[str] = None, language: str = "English") -> str:
    """
    Generate system prompt for the AI assistant
    
    Args:
        country: Selected country for context
        language: Response language
        
    Returns:
        System prompt string
    """
    country_context = f"\n\nCurrent Context: The user is interested in {country}. Provide answers specifically related to {country} when relevant." if country else ""
    
    language_instruction = f"\n\nIMPORTANT: Respond in {language} language. All your responses must be in {language}."
    
    return f"""You are a professional multilingual tourist assistant named "TravelBot". Your job is to guide travelers around the world with expertise and warmth.

Your capabilities:
- Provide detailed travel advice for any country or city
- Recommend tourist attractions (famous landmarks AND hidden gems)
- Suggest hotels and accommodations for different budgets
- Recommend local cuisine and best restaurants
- Provide budget planning and money-saving tips
- Share safety tips and travel precautions
- Explain local customs, culture, and etiquette
- Suggest best times to visit and seasonal activities
- Help with visa requirements and travel documentation
- Provide transportation tips (flights, trains, local transport)
- Recommend shopping areas and local markets
- Share photography spots and scenic viewpoints

Response Style:
- Be friendly, warm, and enthusiastic
- Provide specific, actionable advice
- Use emojis appropriately to make responses engaging
- Give multiple options when possible (budget/mid-range/luxury)
- Include practical tips and insider knowledge
- If unsure, admit it and suggest reliable resources{country_context}{language_instruction}"""


def get_ai_response(user_message: str, country: Optional[str] = None, language: str = "English", chat_history: Optional[List[Dict]] = None) -> str:
    """
    Get AI response using Groq API (Llama 3.1 70B)
    
    Args:
        user_message: User's message
        country: Selected country for context (optional)
        language: Response language (default: English)
        chat_history: Previous conversation history (optional)
        
    Returns:
        AI response text
    """
    # Check if Groq client is available
    if not client:
        return get_fallback_response(user_message, language)
    
    try:
        # Build conversation context
        system_prompt = get_system_prompt(country, language)
        
        # Build messages for Groq chat completion
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add chat history if available (last 6 messages for context)
        if chat_history and len(chat_history) > 0:
            recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
            for msg in recent_history:
                if msg['role'] in ['user', 'assistant']:
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response using Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            top_p=0.9,
            stream=False
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Groq API Error: {str(e)}")
        return get_fallback_response(user_message, language)


def get_fallback_response(user_message: str, language: str = "English") -> str:
    """
    Provide fallback responses when AI is unavailable
    
    Args:
        user_message: User's message
        language: Response language
        
    Returns:
        Fallback response
    """
    
    # Language-specific error messages
    error_messages = {
        "English": "⚠️ **AI Assistant Unavailable**\n\nThe AI assistant requires a valid Groq API key. Please add your GROQ_API_KEY to the .env file.\n\nGet your free API key at: https://console.groq.com/keys",
        "Urdu": "⚠️ **AI اسسٹنٹ دستیاب نہیں**\n\nAI اسسٹنٹ کو Groq API کلید کی ضرورت ہے۔ براہ کرم اپنی GROQ_API_KEY کو .env فائل میں شامل کریں۔",
        "Arabic": "⚠️ **مساعد الذكاء الاصطناعي غير متاح**\n\nيتطلب مساعد الذكاء الاصطناعي مفتاح Groq API صالحًا. يرجى إضافة GROQ_API_KEY إلى ملف .env",
        "French": "⚠️ **Assistant IA indisponible**\n\nL'assistant IA nécessite une clé API Groq valide. Veuillez ajouter votre GROQ_API_KEY au fichier .env",
        "Spanish": "⚠️ **Asistente de IA no disponible**\n\nEl asistente de IA requiere una clave API de Groq válida. Agregue su GROQ_API_KEY al archivo .env",
        "Chinese": "⚠️ **AI助手不可用**\n\nAI助手需要有效的Groq API密钥。请将您的GROQ_API_KEY添加到.env文件中"
    }
    
    return error_messages.get(language, error_messages["English"])


# Keep the existing analyze_budget_input function if it exists below


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
