# 🌍 Travel Budget Planner

A comprehensive fintech travel planning application built with Streamlit, featuring AI assistance, real-time currency conversion, budget tracking, and interactive maps.

## 📋 Features

- **💱 Currency Converter**: Real-time exchange rates for 150+ currencies
- **💰 Trip Budget Calculator**: Plan and track your travel expenses
- **📊 Charts Dashboard**: Visualize your spending patterns and budget allocation
- **🗺️ Tourist Attractions Map**: Discover popular destinations using interactive maps
- **🤖 AI Chatbot Assistant**: Get personalized travel advice and recommendations

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd TrieTech-SIBATHON26
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
TrieTech-SIBATHON26/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Project documentation
├── config/
│   └── settings.py                 # Application configuration
├── pages/
│   ├── 1_💱_Currency_Converter.py
│   ├── 2_💰_Budget_Calculator.py
│   ├── 3_📊_Dashboard.py
│   ├── 4_🗺️_Tourist_Attractions.py
│   └── 5_🤖_AI_Assistant.py
├── utils/
│   ├── __init__.py
│   ├── currency.py                 # Currency conversion logic
│   ├── budget.py                   # Budget calculation logic
│   ├── charts.py                   # Chart generation utilities
│   ├── map_utils.py               # Map utilities
│   └── ai_assistant.py            # AI chatbot logic
├── data/                          # Data storage
└── assets/
    ├── styles.css                  # Custom CSS styling
    └── images/                     # Image assets
```

## 🔑 API Keys Required

- **OpenAI API Key**: For AI assistant functionality
- **Map API Key**: (Optional) For enhanced map features

Add these to your `.env` file:
```
OPENAI_API_KEY=your_openai_key_here
MAP_API_KEY=your_map_api_key_here
```

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Plotly & Matplotlib**: Data visualization
- **Folium**: Interactive maps
- **OpenAI/LangChain**: AI chatbot functionality
- **Forex-Python**: Currency conversion
- **Pandas & NumPy**: Data processing

## 📝 Usage

1. **Currency Converter**: Select source and target currencies to get real-time exchange rates
2. **Budget Calculator**: Input your trip details and expenses to create a comprehensive budget
3. **Dashboard**: View charts and analytics of your budget allocation
4. **Tourist Attractions**: Explore destinations on an interactive map
5. **AI Assistant**: Ask questions about travel planning, budgeting, and destinations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

TrieTech Team - SIBATHON 2026

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- OpenAI for AI capabilities
- All open-source contributors
