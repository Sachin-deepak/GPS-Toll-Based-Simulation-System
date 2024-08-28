import streamlit as st
import random
import simpy
import geopandas as gpd
from geopy.distance import geodesic
import pandas as pd
from shapely.geometry import Polygon, LineString
import math
import folium
from folium.plugins import HeatMap
from streamlit.components.v1 import html as st_html
import random

# defining locations for start and end point
locations_coords = {
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Tiruchirappalli": (10.7905, 78.7047),
    "Salem": (11.6643, 78.1460),
    "Erode": (11.3410, 77.7172),
    "Tirunelveli": (8.7139, 77.7567),
    "Thanjavur": (10.7870, 79.1378),
    "Vellore": (12.9165, 79.1325),
    "Thoothukudi": (8.7642, 78.1348)
}

# defining toll zones
toll_zones = {
    "Toll Zone 1": Polygon([(80.1, 13.0), (80.4, 13.0), (80.4, 13.2), (80.1, 13.2)]),
    "Toll Zone 2": Polygon([(76.8, 11.0), (77.1, 11.0), (77.1, 11.2), (76.8, 11.2)]),
    "Toll Zone 3": Polygon([(78.0, 9.8), (78.3, 9.8), (78.3, 10.0), (78.0, 10.0)]),
    "Toll Zone 4": Polygon([(78.5, 10.6), (78.8, 10.6), (78.8, 10.8), (78.5, 10.8)]),
    "Toll Zone 5": Polygon([(77.5, 12.9), (77.8, 12.9), (77.8, 13.1), (77.5, 13.1)]),
    "Toll Zone 6": Polygon([(78.6, 11.6), (79.0, 11.6), (79.0, 11.8), (78.6, 11.8)])
}

# function to calculate distance between two coordinates using the haversine formula
def calculate_distance(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    radius = 6371  # radius of the earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance

# simulate vehicle movement
def simulate_vehicle_movement(start_loc, end_loc):
    start_coords = locations_coords[start_loc]
    end_coords = locations_coords[end_loc]
    distance = calculate_distance(start_coords, end_coords)
    route = LineString([(start_coords[1], start_coords[0]), (end_coords[1], end_coords[0])])
    toll_zones_passed = []
    toll_zone_distances = []
    for zone, gdf in toll_zones.items():
        if route.intersects(gdf):
            intersection = route.intersection(gdf)
            toll_zones_passed.append(zone)
            toll_zone_distances.append(intersection.length * 111.32)  # conversion of degrees to km
    return distance, toll_zones_passed, toll_zone_distances

# function to calculate toll
def calculate_toll(vehicle_type, toll_zones_passed, toll_zone_distances):
    price_per_km = {
        "Car": 5,
        "Truck": 15,
        "Bike": 2,
        "Bus": 12,
        "Heavy": 20,
        "Ambulance": 0
    }
    fixed_toll_per_zone = {
        "Car": 50,
        "Truck": 150,
        "Bike": 20,
        "Bus": 120,
        "Heavy": 200,
        "Ambulance": 0
    }
    penalty_amount = {
        "Car": 0,
        "Truck": 200,
        "Bike": 0,
        "Bus": 150,
        "Heavy": 300,
        "Ambulance": 0
    }
    toll_waiver = 0  # toll waiver for special cases in INR

    base_toll = sum(toll_zone_distances) * price_per_km[vehicle_type]
    fixed_toll = len(toll_zones_passed) * fixed_toll_per_zone[vehicle_type]
    penalty = penalty_amount[vehicle_type]
    total_toll = base_toll + fixed_toll + penalty - toll_waiver
    return total_toll, base_toll, fixed_toll, penalty

# streamlit UI
st.title("GPS Toll-based system simulation")

vehicle_types = ["Car", "Truck", "Bike", "Bus", "Heavy", "Ambulance"]
vehicle_type = st.selectbox("Select Vehicle Type", vehicle_types)

start_loc = st.selectbox("Select Start Location", list(locations_coords.keys()))
end_loc = st.selectbox("Select End Location", list(locations_coords.keys()))

if st.button("Calculate Toll"):
    distance, toll_zones_passed, toll_zone_distances = simulate_vehicle_movement(start_loc, end_loc)
    total_toll, base_toll, fixed_toll, penalty = calculate_toll(vehicle_type, toll_zones_passed, toll_zone_distances)

    st.write(f"Vehicle Type: {vehicle_type}")
    st.write(f"Start Location: {start_loc}")
    st.write(f"End Location: {end_loc}")
    st.write(f"Total Distance: {distance:.2f} km")
    st.write(f"Toll Zones Passed: {', '.join(toll_zones_passed)}")
    st.write(f"Base Toll (Distance Based): {base_toll:.2f} INR")
    st.write(f"Fixed Toll (Per Zone): {fixed_toll:.2f} INR")
    st.write(f"Penalty: {penalty:.2f} INR")
    st.write(f"Total Toll: {total_toll:.2f} INR")

    # display the map
    start_coords = locations_coords[start_loc]
    end_coords = locations_coords[end_loc]
    m = folium.Map(location=[(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2], zoom_start=7)
    folium.Marker(location=start_coords, popup=start_loc, icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(location=end_coords, popup=end_loc, icon=folium.Icon(color="red")).add_to(m)
    folium.PolyLine(locations=[start_coords, end_coords], color="blue").add_to(m)

    for zone, coords in toll_zones.items():
        folium.GeoJson(coords, name=zone).add_to(m)
        zone_center = [coords.bounds[1] + (coords.bounds[3] - coords.bounds[1]) / 2, coords.bounds[0] + (coords.bounds[2] - coords.bounds[0]) / 2]
        folium.Marker(location=zone_center, popup=zone, icon=folium.Icon()).add_to(m)

    heatmap_data = [(coords[0], coords[1], random.uniform(0, 1)) for coords in locations_coords.values()]
    HeatMap(heatmap_data).add_to(m)

    st_html(m._repr_html_(), height=500)
