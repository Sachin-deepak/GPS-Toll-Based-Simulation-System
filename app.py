import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import requests
import polyline

# Set page config
st.set_page_config(page_title="GPS Toll-based system simulation", layout="wide")

# Title and description
st.title("GPS Toll-based system simulation")
st.markdown("Calculate toll charges across different locations in Tamil Nadu")

LOCATIONS = {
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Salem": (11.6643, 78.1460),
    "Tiruchirappalli": (10.7905, 78.7047),
    "Tirunelveli": (8.7139, 77.7567),
    "Erode": (11.3410, 77.7172),
    "Vellore": (12.9165, 79.1325),
    "Thanjavur": (10.7869, 79.1378),
    "Hosur": (12.7406, 77.8252)
}

# Vehicle types and their base rates (per km)
VEHICLE_RATES = {
    "Two Wheeler": 0.5,
    "Car/Jeep/Van": 1.0,
    "Bus": 2.0,
    "Truck": 3.0,
    "Multi-Axle Vehicle": 4.0
}

def get_route_coordinates(start_coords, end_coords):
    """Get actual route coordinates using OSRM"""
    try:
        # Format coordinates for OSRM API
        start_lon, start_lat = start_coords[1], start_coords[0]
        end_lon, end_lat = end_coords[1], end_coords[0]
        
        # Make request to OSRM API
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=polyline"
        response = requests.get(url)
        data = response.json()
        
        if data["code"] == "Ok":
            # Decode polyline to get route coordinates
            route_polyline = data["routes"][0]["geometry"]
            route_coords = polyline.decode(route_polyline)
            # Convert to (lat, lon) format for folium
            route_coords = [(coord[0], coord[1]) for coord in route_coords]
            distance = data["routes"][0]["distance"] / 1000  # Convert to kilometers
            duration = data["routes"][0]["duration"] / 60  # Convert to minutes
            return route_coords, distance, duration
        else:
            # Fallback to straight line if routing fails
            return [start_coords, end_coords], geodesic(start_coords, end_coords).kilometers, None
    except Exception as e:
        st.warning(f"Could not fetch precise route. Using straight line instead. Error: {str(e)}")
        return [start_coords, end_coords], geodesic(start_coords, end_coords).kilometers, None

# Create two columns for source and destination selection
col1, col2 = st.columns(2)

with col1:
    source = st.selectbox("Select Source Location", list(LOCATIONS.keys()))
    
with col2:
    destination = st.selectbox("Select Destination Location", list(LOCATIONS.keys()))

# Vehicle type selection
vehicle_type = st.selectbox("Select Vehicle Type", list(VEHICLE_RATES.keys()))

# Additional options
col3, col4 = st.columns(2)
with col3:
    is_ambulance = st.checkbox("Ambulance (Free Toll)")
with col4:
    has_penalty = st.checkbox("Late Payment (20% penalty)")

# Calculate distance and toll
def calculate_toll(source, destination, vehicle_type, is_ambulance, has_penalty):
    source_coords = LOCATIONS[source]
    dest_coords = LOCATIONS[destination]
    
    # Get actual route and distance
    route_coords, distance, duration = get_route_coordinates(source_coords, dest_coords)
    
    # Base toll calculation
    base_rate = VEHICLE_RATES[vehicle_type]
    base_toll = distance * base_rate
    
    # Apply discounts and penalties
    if is_ambulance:
        base_toll = 0  # Free for ambulance
    
    if has_penalty:
        base_toll *= 1.2  # 20% penalty for late payment
    
    return distance, base_toll, route_coords, duration

# Calculate and display results
if source != destination:
    distance, toll, route_coords, duration = calculate_toll(source, destination, vehicle_type, is_ambulance, has_penalty)
    
    # Display results
    st.markdown("---")
    st.subheader("Journey Details")
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Distance", f"{distance:.2f} km")
    with col6:
        st.metric("Toll Amount", f"₹{toll:.2f}")
    with col7:
        if duration:
            st.metric("Estimated Duration", f"{duration:.0f} minutes")
    
    # Create map
    st.subheader("Route Map")
    m = folium.Map(location=[LOCATIONS[source][0], LOCATIONS[source][1]], zoom_start=7)
    
    # Add markers for source and destination
    folium.Marker(
        LOCATIONS[source],
        popup=f"Source: {source}",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)
    
    folium.Marker(
        LOCATIONS[destination],
        popup=f"Destination: {destination}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Add the actual route with gradient colors based on distance
    folium.PolyLine(
        locations=route_coords,
        color='blue',
        weight=3,
        opacity=0.8,
        popup=f"Distance: {distance:.2f} km\nDuration: {duration:.0f} minutes" if duration else f"Distance: {distance:.2f} km"
    ).add_to(m)
    
    # Display the map
    folium_static(m)
    
    # Additional information
    st.markdown("---")
    st.subheader("Additional Information")
    st.markdown("""
    - Base rates are calculated per kilometer
    - Ambulance vehicles are exempt from toll charges
    - Late payment incurs 20% penalty
    - Routes are calculated using actual road networks
    - Estimated duration is based on current traffic conditions
    - Rates may vary based on time of day and special conditions
    """)
else:
    st.warning("Please select different source and destination locations") 
