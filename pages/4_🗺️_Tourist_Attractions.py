"""
Tourist Attractions Map Page
Interactive map showing tourist destinations and attractions
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.map_utils import create_base_map, add_markers, search_attractions
from config.settings import DEFAULT_MAP_CENTER, DEFAULT_MAP_ZOOM

st.set_page_config(page_title="Tourist Attractions", page_icon="🗺️", layout="wide")

st.title("🗺️ Tourist Attractions Map")
st.markdown("Discover popular destinations and attractions around the world")

# Search and filter section
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_location = st.text_input(
        "🔍 Search Location",
        placeholder="Enter city, country, or attraction name..."
    )

with col2:
    map_style = st.selectbox(
        "Map Style",
        ["OpenStreetMap", "Satellite", "Terrain"]
    )

with col3:
    show_markers = st.checkbox("Show Attractions", value=True)

# Popular destinations with coordinates
POPULAR_DESTINATIONS = {
    "Paris, France": {"lat": 48.8566, "lon": 2.3522, "attractions": [
        {"name": "Eiffel Tower", "lat": 48.8584, "lon": 2.2945, "type": "Monument"},
        {"name": "Louvre Museum", "lat": 48.8606, "lon": 2.3376, "type": "Museum"},
        {"name": "Notre-Dame", "lat": 48.8530, "lon": 2.3499, "type": "Cathedral"},
    ]},
    "Tokyo, Japan": {"lat": 35.6762, "lon": 139.6503, "attractions": [
        {"name": "Tokyo Tower", "lat": 35.6586, "lon": 139.7454, "type": "Monument"},
        {"name": "Senso-ji Temple", "lat": 35.7148, "lon": 139.7967, "type": "Temple"},
        {"name": "Shibuya Crossing", "lat": 35.6595, "lon": 139.7004, "type": "Landmark"},
    ]},
    "New York, USA": {"lat": 40.7128, "lon": -74.0060, "attractions": [
        {"name": "Statue of Liberty", "lat": 40.6892, "lon": -74.0445, "type": "Monument"},
        {"name": "Central Park", "lat": 40.7829, "lon": -73.9654, "type": "Park"},
        {"name": "Empire State Building", "lat": 40.7484, "lon": -73.9857, "type": "Building"},
    ]},
    "London, UK": {"lat": 51.5074, "lon": -0.1278, "attractions": [
        {"name": "Big Ben", "lat": 51.5007, "lon": -0.1246, "type": "Monument"},
        {"name": "Tower Bridge", "lat": 51.5055, "lon": -0.0754, "type": "Bridge"},
        {"name": "British Museum", "lat": 51.5194, "lon": -0.1270, "type": "Museum"},
    ]},
    "Dubai, UAE": {"lat": 25.2048, "lon": 55.2708, "attractions": [
        {"name": "Burj Khalifa", "lat": 25.1972, "lon": 55.2744, "type": "Building"},
        {"name": "Dubai Mall", "lat": 25.1981, "lon": 55.2796, "type": "Shopping"},
        {"name": "Palm Jumeirah", "lat": 25.1124, "lon": 55.1390, "type": "Island"},
    ]},
    "Sydney, Australia": {"lat": -33.8688, "lon": 151.2093, "attractions": [
        {"name": "Opera House", "lat": -33.8568, "lon": 151.2153, "type": "Building"},
        {"name": "Harbour Bridge", "lat": -33.8523, "lon": 151.2108, "type": "Bridge"},
        {"name": "Bondi Beach", "lat": -33.8908, "lon": 151.2743, "type": "Beach"},
    ]},
}

# Quick select popular destinations
st.subheader("🌟 Popular Destinations")
selected_destination = st.selectbox(
    "Quick Select",
    [""] + list(POPULAR_DESTINATIONS.keys())
)

# Initialize map center and zoom
if selected_destination and selected_destination in POPULAR_DESTINATIONS:
    dest_info = POPULAR_DESTINATIONS[selected_destination]
    center_lat = dest_info["lat"]
    center_lon = dest_info["lon"]
    zoom = 12
    attractions = dest_info["attractions"]
else:
    center_lat = DEFAULT_MAP_CENTER[0]
    center_lon = DEFAULT_MAP_CENTER[1]
    zoom = DEFAULT_MAP_ZOOM
    attractions = []

# Create the map
st.markdown("---")

# Map tiles based on style
tile_map = {
    "OpenStreetMap": "OpenStreetMap",
    "Satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    "Terrain": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}"
}

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=zoom,
    tiles=tile_map.get(map_style, "OpenStreetMap"),
    attr="Map data"
)

# Add destination marker
if selected_destination:
    folium.Marker(
        [center_lat, center_lon],
        popup=f"<b>{selected_destination}</b>",
        tooltip=selected_destination,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Add attraction markers
if show_markers and attractions:
    for attraction in attractions:
        icon_color_map = {
            "Monument": "blue",
            "Museum": "green",
            "Temple": "purple",
            "Park": "lightgreen",
            "Building": "darkblue",
            "Beach": "lightblue",
            "Bridge": "orange",
            "Cathedral": "purple",
            "Landmark": "red",
            "Shopping": "pink",
            "Island": "cadetblue"
        }
        
        folium.Marker(
            [attraction["lat"], attraction["lon"]],
            popup=f"<b>{attraction['name']}</b><br>Type: {attraction['type']}",
            tooltip=attraction["name"],
            icon=folium.Icon(
                color=icon_color_map.get(attraction["type"], "gray"),
                icon="star"
            )
        ).add_to(m)

# Display map
st_data = st_folium(m, width=None, height=600)

# Display attraction list
if selected_destination and attractions:
    st.markdown("---")
    st.subheader(f"📍 Attractions in {selected_destination}")
    
    for i, attraction in enumerate(attractions, 1):
        col_a, col_b, col_c = st.columns([2, 1, 1])
        with col_a:
            st.markdown(f"**{i}. {attraction['name']}**")
        with col_b:
            st.markdown(f"*{attraction['type']}*")
        with col_c:
            st.markdown(f"📍 [{attraction['lat']:.4f}, {attraction['lon']:.4f}]")

# Information panel
st.markdown("---")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. Select a popular destination from the dropdown
    2. Toggle attraction markers on/off
    3. Click on markers for more information
    4. Zoom in/out using the map controls
    5. Switch between different map styles
    """)

with col_info2:
    st.markdown("### 💡 Travel Tips")
    st.markdown("""
    - Research attractions before your trip
    - Check opening hours and ticket prices
    - Book popular attractions in advance
    - Consider travel time between locations
    - Look for combination tickets for savings
    """)

# Statistics
if selected_destination:
    st.markdown("---")
    st.subheader("📊 Quick Stats")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Attractions", len(attractions))
    
    with stat_col2:
        attraction_types = set([a["type"] for a in attractions])
        st.metric("Categories", len(attraction_types))
    
    with stat_col3:
        st.metric("City", selected_destination.split(",")[0])
    
    with stat_col4:
        st.metric("Map Zoom", zoom)
