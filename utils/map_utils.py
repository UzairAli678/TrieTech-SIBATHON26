"""
Map utilities
Handles map creation and location services
"""

import folium
import requests
from typing import Dict, List, Tuple, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def create_base_map(
    center: List[float],
    zoom: int = 10,
    tiles: str = "OpenStreetMap"
) -> folium.Map:
    """
    Create a base folium map
    
    Args:
        center: [latitude, longitude]
        zoom: Initial zoom level
        tiles: Map tile style
        
    Returns:
        Folium map object
    """
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=tiles
    )
    
    return m


def add_markers(
    map_obj: folium.Map,
    locations: List[Dict],
    icon_color: str = "blue"
) -> folium.Map:
    """
    Add markers to a map
    
    Args:
        map_obj: Folium map object
        locations: List of location dictionaries with 'lat', 'lon', 'name', 'info'
        icon_color: Marker color
        
    Returns:
        Updated map object
    """
    for loc in locations:
        folium.Marker(
            location=[loc["lat"], loc["lon"]],
            popup=folium.Popup(loc.get("info", loc["name"]), max_width=300),
            tooltip=loc["name"],
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(map_obj)
    
    return map_obj


def geocode_location(location_name: str) -> Optional[Tuple[float, float]]:
    """
    Convert location name to coordinates
    
    Args:
        location_name: Name of location (city, country, address)
        
    Returns:
        Tuple of (latitude, longitude) or None
    """
    try:
        geolocator = Nominatim(user_agent="travel_budget_planner")
        location = geolocator.geocode(location_name, timeout=10)
        
        if location:
            return (location.latitude, location.longitude)
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    
    return None


def reverse_geocode(lat: float, lon: float) -> Optional[str]:
    """
    Convert coordinates to location name
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Location name or None
    """
    try:
        geolocator = Nominatim(user_agent="travel_budget_planner")
        location = geolocator.reverse(f"{lat}, {lon}", timeout=10)
        
        if location:
            return location.address
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    
    return None


def get_places(city: str, api_key: str) -> Optional[Dict]:
    """
    Fetch tourist places from Geoapify Places API with enhanced data
    
    Args:
        city: City name to search
        api_key: Geoapify API key
        
    Returns:
        Dict with center coordinates and list of places
    """
    import random
    
    if not api_key:
        return None
        
    try:
        # First, geocode the city to get coordinates
        geocode_url = "https://api.geoapify.com/v1/geocode/search"
        geocode_params = {
            "text": city,
            "apiKey": api_key,
            "limit": 1
        }
        
        geo_response = requests.get(geocode_url, params=geocode_params, timeout=30)
        
        if geo_response.status_code != 200:
            return None
            
        geo_data = geo_response.json()
        
        if not geo_data.get("features"):
            return None
            
        coordinates = geo_data["features"][0]["geometry"]["coordinates"]
        lon, lat = coordinates[0], coordinates[1]
        
        # Fetch places with larger radius and limit
        places_url = "https://api.geoapify.com/v2/places"
        places_params = {
            "categories": "tourism,heritage,entertainment.museum,tourism.attraction,tourism.sights,entertainment.culture",
            "filter": f"circle:{lon},{lat},10000",
            "limit": 40,
            "apiKey": api_key
        }
        
        places_response = requests.get(places_url, params=places_params, timeout=30)
        
        if places_response.status_code != 200:
            return None
            
        places_data = places_response.json()
        
        if not places_data.get("features"):
            return {"center": [lat, lon], "places": []}
            
        # Parse places
        all_places = []
        seen_names = set()
        
        for feature in places_data["features"]:
            props = feature.get("properties", {})
            coords = feature.get("geometry", {}).get("coordinates", [0, 0])
            name = props.get("name", "Unknown Place")
            
            # Remove duplicates
            if name in seen_names:
                continue
            seen_names.add(name)
            
            categories = props.get("categories", ["tourism"])
            main_category = categories[0] if categories else "tourism"
            
            # Prioritize tourism categories
            is_tourism = "tourism" in main_category or "attraction" in main_category
            
            place = {
                "name": name,
                "lat": coords[1],
                "lon": coords[0],
                "address": props.get("formatted", "Address not available"),
                "category": main_category,
                "description": props.get("description", ""),
                "website": props.get("datasource", {}).get("raw", {}).get("website", ""),
                "priority": 1 if is_tourism else 0
            }
            all_places.append(place)
        
        # Sort by priority and randomly select 20
        all_places.sort(key=lambda x: x["priority"], reverse=True)
        tourism_places = [p for p in all_places if p["priority"] == 1]
        other_places = [p for p in all_places if p["priority"] == 0]
        
        # Take up to 15 tourism places and up to 5 others
        selected = tourism_places[:15] + other_places[:5]
        
        # If we have more than 20, randomly sample
        if len(selected) > 20:
            selected = random.sample(selected, 20)
        
        # Remove priority field from final result
        for place in selected:
            place.pop("priority", None)
            
        return {
            "center": [lat, lon],
            "places": selected
        }
        
    except Exception as e:
        print(f"Error fetching places: {e}")
        return None


def search_attractions(
    location: str,
    category: str = "tourist_attraction"
) -> List[Dict]:
    """
    Search for attractions near a location
    
    Note: This is a placeholder. In production, integrate with
    Google Places API, Foursquare, or similar service.
    
    Args:
        location: Location name
        category: Type of attraction
        
    Returns:
        List of attraction dictionaries
    """
    # Placeholder implementation
    # In production, integrate with an actual API
    
    sample_attractions = [
        {
            "name": "Sample Attraction 1",
            "lat": 0.0,
            "lon": 0.0,
            "type": category,
            "rating": 4.5,
            "description": "A popular tourist attraction"
        }
    ]
    
    return sample_attractions


def calculate_distance(
    point1: Tuple[float, float],
    point2: Tuple[float, float]
) -> float:
    """
    Calculate distance between two points using Haversine formula
    
    Args:
        point1: (latitude, longitude) of first point
        point2: (latitude, longitude) of second point
        
    Returns:
        Distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    
    lat1, lon1 = point1
    lat2, lon2 = point2
    
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    
    return distance


def add_route(
    map_obj: folium.Map,
    waypoints: List[Tuple[float, float]],
    color: str = "blue",
    weight: int = 5
) -> folium.Map:
    """
    Add a route line between waypoints
    
    Args:
        map_obj: Folium map object
        waypoints: List of (latitude, longitude) tuples
        color: Line color
        weight: Line thickness
        
    Returns:
        Updated map object
    """
    folium.PolyLine(
        locations=waypoints,
        color=color,
        weight=weight,
        opacity=0.8
    ).add_to(map_obj)
    
    return map_obj


def add_circle(
    map_obj: folium.Map,
    center: Tuple[float, float],
    radius: float,
    color: str = "blue",
    fill: bool = True
) -> folium.Map:
    """
    Add a circle to the map
    
    Args:
        map_obj: Folium map object
        center: (latitude, longitude) of circle center
        radius: Radius in meters
        color: Circle color
        fill: Whether to fill the circle
        
    Returns:
        Updated map object
    """
    folium.Circle(
        location=center,
        radius=radius,
        color=color,
        fill=fill,
        fillColor=color,
        fillOpacity=0.2
    ).add_to(map_obj)
    
    return map_obj
