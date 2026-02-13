"""
Map utilities
Handles map creation and location services
"""

import folium
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
