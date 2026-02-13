"""
AI Assistant Page
Chatbot for travel planning advice and recommendations
"""

import streamlit as st
from datetime import datetime
from utils.ai_assistant import get_ai_response, initialize_conversation

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Travel Assistant")
st.markdown("Get personalized travel advice, tips, and recommendations")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "Hello! 👋 I'm your AI travel assistant. I can help you with:\n\n"
                   "- Travel destination recommendations\n"
                   "- Budget planning advice\n"
                   "- Packing tips\n"
                   "- Best times to visit\n"
                   "- Local customs and culture\n"
                   "- Safety tips\n\n"
                   "What would you like to know about your trip?",
        "timestamp": datetime.now()
    })

# Sidebar with suggestions
with st.sidebar:
    st.header("💡 Quick Questions")
    
    sample_questions = [
        "What's the best time to visit Paris?",
        "How much should I budget for a week in Tokyo?",
        "What are must-see attractions in Rome?",
        "Tips for traveling on a budget?",
        "What should I pack for a beach vacation?",
        "How to stay safe while traveling?",
        "Best food to try in Thailand?",
        "Currency tips for international travel?"
    ]
    
    st.markdown("Click a question to ask:")
    for question in sample_questions:
        if st.button(question, key=f"q_{hash(question)}", use_container_width=True):
            st.session_state.user_input = question
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": "Chat cleared! How can I help you with your travel plans?",
            "timestamp": datetime.now()
        }]
        st.rerun()
    
    st.markdown("---")
    st.info("""
    **Note**: This AI assistant provides general travel advice. 
    Always verify important information with official sources.
    """)

# Main chat interface
st.markdown("---")

# Display chat history
chat_container = st.container()

with chat_container:
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", datetime.now())
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
                st.caption(timestamp.strftime("%H:%M:%S"))
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)
                st.caption(timestamp.strftime("%H:%M:%S"))

# Chat input
user_input = st.chat_input("Type your travel question here...")

# Handle pre-filled input from sidebar
if "user_input" in st.session_state and st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = None

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Get AI response
    with st.spinner("Thinking..."):
        response = get_ai_response(user_input, st.session_state.chat_history)
    
    # Add assistant response to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now()
    })
    
    st.rerun()

# Travel tips section
st.markdown("---")

with st.expander("📚 Travel Planning Resources"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎒 Pre-Trip Planning
        - Research visa requirements
        - Check passport validity (6+ months)
        - Get travel insurance
        - Notify your bank
        - Make copies of important documents
        - Learn basic local phrases
        """)
    
    with col2:
        st.markdown("""
        ### 🛡️ Safety Tips
        - Register with your embassy
        - Keep emergency contacts handy
        - Use secure accommodation
        - Avoid displaying valuables
        - Stay aware of your surroundings
        - Keep digital copies of documents
        """)

with st.expander("💰 Money-Saving Tips"):
    st.markdown("""
    - **Book in advance**: Flights and hotels are usually cheaper when booked early
    - **Travel off-season**: Avoid peak tourist seasons for better prices
    - **Use public transport**: Much cheaper than taxis or rental cars
    - **Eat local**: Street food and local restaurants are authentic and affordable
    - **Free attractions**: Many cities offer free museums, parks, and walking tours
    - **Travel cards**: Get city passes for unlimited transport and attraction discounts
    - **Cook occasionally**: Book accommodation with kitchen facilities
    - **Walk when possible**: Best way to explore and it's free!
    """)

with st.expander("🌍 Popular Destinations by Region"):
    tab1, tab2, tab3, tab4 = st.tabs(["Europe", "Asia", "Americas", "Other"])
    
    with tab1:
        st.markdown("""
        **Popular European Destinations:**
        - 🇫🇷 Paris, France - Art, culture, cuisine
        - 🇮🇹 Rome, Italy - History, architecture
        - 🇬🇧 London, UK - Museums, royal heritage
        - 🇪🇸 Barcelona, Spain - Beaches, Gaudí
        - 🇬🇷 Athens, Greece - Ancient ruins
        """)
    
    with tab2:
        st.markdown("""
        **Popular Asian Destinations:**
        - 🇯🇵 Tokyo, Japan - Technology, tradition
        - 🇹🇭 Bangkok, Thailand - Temples, street food
        - 🇸🇬 Singapore - Modern city-state
        - 🇮🇳 Delhi, India - Culture, history
        - 🇨🇳 Beijing, China - Great Wall, palaces
        """)
    
    with tab3:
        st.markdown("""
        **Popular American Destinations:**
        - 🇺🇸 New York, USA - Iconic skyline
        - 🇲🇽 Cancun, Mexico - Beaches, ruins
        - 🇧🇷 Rio, Brazil - Carnival, beaches
        - 🇨🇦 Vancouver, Canada - Nature, city life
        - 🇦🇷 Buenos Aires, Argentina - Tango, culture
        """)
    
    with tab4:
        st.markdown("""
        **Other Popular Destinations:**
        - 🇦🇪 Dubai, UAE - Luxury, modern architecture
        - 🇦🇺 Sydney, Australia - Opera House, beaches
        - 🇿🇦 Cape Town, South Africa - Nature, wildlife
        - 🇪🇬 Cairo, Egypt - Pyramids, history
        - 🇳🇿 Auckland, New Zealand - Adventure sports
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 Powered by AI | Responses are AI-generated and should be verified</p>
</div>
""", unsafe_allow_html=True)
