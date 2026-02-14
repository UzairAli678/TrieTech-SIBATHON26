"""
TriEtech Tourist Attractions Explorer
Professional destination discovery with interactive maps and comprehensive place information
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os
from dotenv import load_dotenv
from utils.budget import fetch_countries
from folium.plugins import MarkerCluster, Fullscreen, MiniMap
import time

load_dotenv()

st.set_page_config(page_title="TriEtech Tourist Attractions", page_icon="🗺️", layout="wide")

# Initialize theme from main app
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Dynamic theming
theme = st.session_state.theme
if theme == "dark":
    bg_color = "#0E1117"
    secondary_bg = "#1E2530"
    card_bg = "#262C3A"
    text_color = "#FFFFFF"
    text_secondary = "#B0B8C5"
    border_color = "#3A4052"
    shadow = "rgba(0, 0, 0, 0.5)"
else:
    bg_color = "#FFFFFF"
    secondary_bg = "#F7F9FC"
    card_bg = "#FFFFFF"
    text_color = "#1A202C"
    text_secondary = "#4A5568"
    border_color = "#E2E8F0"
    shadow = "rgba(0, 0, 0, 0.1)"

# Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {bg_color};
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: {secondary_bg};
        border-right: 1px solid {border_color};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    
    /* Header Styling */
    header[data-testid="stHeader"] {{
        background: {secondary_bg};
        border-bottom: 1px solid {border_color};
    }}
    
    .main-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
    }}
    
    .main-header h1 {{
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }}
    
    .main-header p {{
        margin: 1rem 0 0 0;
        font-size: 1.25rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }}
    
    .place-card {{
        background: {card_bg};
        padding: 1.25rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }}
    
    .place-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }}
    
    .place-name {{
        font-weight: 700;
        font-size: 1.125rem;
        color: {text_color};
        margin-bottom: 0.5rem;
    }}
    
    .place-address {{
        font-size: 0.9375rem;
        color: {text_secondary};
        line-height: 1.6;
    }}
    
    .stat-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(102, 126, 234, 0.4);
    }}
    
    .stat-number {{
        font-size: 2.25rem;
        font-weight: 800;
    }}
    
    .stat-label {{
        font-size: 0.875rem;
        opacity: 0.95;
        margin-top: 0.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    div.stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
    }}
    
    /* Hide Main Menu */
    #MainMenu {{visibility: hidden;}}
    
    /* Footer */
    footer {{
        visibility: visible !important;
        background: {secondary_bg};
        border-top: 1px solid {border_color};
        padding: 1.5rem 0;
        margin-top: 3rem;
    }}
    
    footer * {{
        color: {text_secondary} !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {secondary_bg};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: #667eea;
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #764ba2;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
if "countries_list" not in st.session_state:
    st.session_state.countries_list = None
if "map_data" not in st.session_state:
    st.session_state.map_data = None

# Header
st.markdown("""
<div class="main-header">
    <h1 style='margin: 0; font-size: 48px; font-weight: 700;'>TriEtech Tourist Attractions</h1>
    <p style='margin: 15px 0 0 0; font-size: 18px; opacity: 0.95;'>
        Discover top attractions worldwide with comprehensive information and interactive maps
    </p>
</div>
""", unsafe_allow_html=True)

# Load countries
if st.session_state.countries_list is None:
    with st.spinner("Loading countries data..."):
        st.session_state.countries_list = fetch_countries()

countries = st.session_state.countries_list
api_key = os.getenv("GEOAPIFY_API_KEY", "")

if not api_key:
    st.error("⚠️ Geoapify API key not found. Add GEOAPIFY_API_KEY to .env file.")
    st.stop()

# Two-column layout
col_sidebar, col_main = st.columns([1, 2.5])

with col_sidebar:
    st.markdown("### 🌍 Select Country")
    
    country_options = [f"{c['flag']} {c['name']}" for c in countries]
    
    selected_country_display = st.selectbox(
        "Choose a country",
        ["-- Select Country --"] + country_options,
        label_visibility="collapsed"
    )
    
    search_query = None
    if selected_country_display != "-- Select Country --":
        selected_idx = country_options.index(selected_country_display)
        selected_country_data = countries[selected_idx]
        country_name = selected_country_data['name']
        
        # Use capital cities for better results
        capital_map = {
            "Pakistan": "Islamabad, Pakistan",
            "India": "New Delhi, India",
            "United States": "New York, United States",
            "United Kingdom": "London, United Kingdom",
            "France": "Paris, France",
            "Japan": "Tokyo, Japan",
            "Germany": "Berlin, Germany",
            "Italy": "Rome, Italy",
            "Spain": "Madrid, Spain",
            "Australia": "Sydney, Australia",
            "Turkey": "Istanbul, Turkey",
            "Thailand": "Bangkok, Thailand",
            "United Arab Emirates": "Dubai, United Arab Emirates",
            "China": "Beijing, China",
            "Brazil": "Rio de Janeiro, Brazil",
            "Mexico": "Mexico City, Mexico",
            "Canada": "Toronto, Canada",
        }
        
        search_query = capital_map.get(country_name, country_name)
        
        st.success(f"{selected_country_data['flag']} {country_name}")
    
    if st.button("Explore Attractions", use_container_width=True, type="primary", disabled=(search_query is None)):
        st.session_state.map_data = None  # Trigger fresh search
        st.rerun()
    
    if st.button("Reset", use_container_width=True):
        st.session_state.selected_country = None
        st.session_state.map_data = None
        st.rerun()
    
    # Quick access buttons
    st.markdown("---")
    st.markdown("### Quick Access")
    
    quick_access = {
        "France": "Paris, France",
        "Japan": "Tokyo, Japan",
        "USA": "New York, United States",
        "UK": "London, United Kingdom",
        "Pakistan": "Islamabad, Pakistan",
        "UAE": "Dubai, United Arab Emirates",
        "Italy": "Rome, Italy",
        "Turkey": "Istanbul, Turkey",
    }
    
    for label, query in quick_access.items():
        if st.button(label, use_container_width=True, key=label):
            st.session_state.temp_query = query
            st.session_state.map_data = None
            st.rerun()
    
    # Display places list if data exists
    if st.session_state.map_data:
        places = st.session_state.map_data.get("places", [])
        if places:
            st.markdown("---")
            st.markdown(f"### {len(places)} Places Found")
            
            for idx, place in enumerate(places, 1):
                st.markdown(f"""
                <div class="place-card">
                    <div class="place-name">{idx}. {place['name']}</div>
                    <div class="place-address">{place.get('address', 'Address not available')[:80]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Category:** {place.get('category', 'N/A')}")
                        st.write(f"**Address:** {place.get('address', 'N/A')}")
                    with col2:
                        st.write(f"**Coordinates:** {place['lat']: .5f}, {place['lon']:.5f}")
                        maps_url = f"https://www.google.com/maps?q={place['lat']},{place['lon']}"
                        st.markdown(f"[Open in Google Maps]({maps_url})")

with col_main:
    # Determine what to search
    final_search = None
    if hasattr(st.session_state, 'temp_query') and st.session_state.temp_query:
        final_search = st.session_state.temp_query
        st.session_state.temp_query = None  # Clear after use
    elif search_query:
        final_search = search_query
    
    # Fetch data if needed
    if final_search and not st.session_state.map_data:
        with st.spinner(f"Discovering top attractions in {final_search}..."):
            try:
                # Geocode and fetch places
                geocode_url = "https://api.geoapify.com/v1/geocode/search"
                geocode_params = {"text": final_search, "apiKey": api_key, "limit": 1}
                
                geo_response = requests.get(geocode_url, params=geocode_params, timeout=15)
                
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    
                    if geo_data.get("features"):
                        coordinates = geo_data["features"][0]["geometry"]["coordinates"]
                        lon, lat = coordinates[0], coordinates[1]
                        
                        # Fetch places
                        places_url = "https://api.geoapify.com/v2/places"
                        places_params = {
                            "categories": "tourism,heritage,entertainment,natural,leisure",
                            "filter": f"circle:{lon},{lat},25000",
                            "bias": f"proximity:{lon},{lat}",
                            "limit": 40,
                            "apiKey": api_key
                        }
                        
                        places_response = requests.get(places_url, params=places_params, timeout=15)
                        
                        if places_response.status_code == 200:
                            places_data = places_response.json()
                            features = places_data.get("features", [])
                            
                            places = []
                            for feature in features:
                                props = feature["properties"]
                                geom = feature["geometry"]["coordinates"]
                                
                                # Get the place name
                                place_name = props.get("name", "").strip()
                                
                                # Skip places without proper names or generic names
                                if not place_name or place_name.lower() in ["unnamed", "unknown", "", "n/a"]:
                                    continue
                                
                                # Skip if name is too short (likely invalid)
                                if len(place_name) < 2:
                                    continue
                                
                                places.append({
                                    "name": place_name,
                                    "category": props.get("categories", ["unknown"])[0] if props.get("categories") else "unknown",
                                    "address": props.get("formatted", "Address not available"),
                                    "lat": geom[1],
                                    "lon": geom[0]
                                })
                                
                                # Stop after collecting 20 valid places
                                if len(places) >= 20:
                                    break
                            
                            if places:
                                st.session_state.map_data = {
                                    "center": [lat, lon],
                                    "places": places
                                }
                                st.rerun()
                            else:
                                st.warning(f"No attractions found with valid names in this area. Try a different location.")
                        else:
                            st.error("Failed to fetch places data.")
                    else:
                        st.warning(f"Could not locate '{final_search}'. Try another name.")
                else:
                    st.error("Geocoding failed. Please try again.")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display map
    if st.session_state.map_data:
        places = st.session_state.map_data.get("places", [])
        center = st.session_state.map_data.get("center", [0, 0])
        
        if places:
            # Stats
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(places)}</div>
                    <div class="stat-label">ATTRACTIONS</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s2:
                categories = len(set([p["category"] for p in places]))
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{categories}</div>
                    <div class="stat-label">CATEGORIES</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">MAP</div>
                    <div class="stat-label">INTERACTIVE</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Map
            st.markdown("### Interactive Map")
            
            m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap")
            
            marker_cluster = MarkerCluster().add_to(m)
            
            for idx, place in enumerate(places, 1):
                popup_html = f"""
                <div style='font-family: Inter; min-width: 250px;'>
                    <h4 style='color: #667eea; margin: 0 0 8px 0;'>{idx}. {place['name']}</h4>
                    <p style='margin: 4px 0; font-size: 13px;'><b>Location:</b> {place['address'][:80]}</p>
                    <p style='margin: 4px 0; font-size: 12px; color: #666;'><b>Category:</b> {place['category']}</p>
                </div>
                """
                
                folium.Marker(
                    location=[place["lat"], place["lon"]],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{idx}. {place['name']}",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(marker_cluster)
            
            Fullscreen().add_to(m)
            MiniMap().add_to(m)
            
            st_folium(m, width=None, height=600)
            
            st.info("**🎮 Map Controls:** Drag to pan • Scroll to zoom • Click markers for details")
    
    else:
        # Welcome message
        st.markdown("""
        <div style='text-align: center; padding: 80px 40px; background: #f7fafc; border-radius: 20px;'>
            <div style='font-size: 80px; margin-bottom: 20px;'>🌍</div>
            <h2 style='color: #2d3748; margin-bottom: 16px;'>Discover Amazing Places</h2>
            <p style='color: #718096; font-size: 18px; max-width: 600px; margin: 0 auto;'>
                Select a country from the dropdown or use quick access buttons to explore
                the top 20 tourist attractions with interactive maps and detailed information.
            </p>
        </div>
        """, unsafe_allow_html=True)
