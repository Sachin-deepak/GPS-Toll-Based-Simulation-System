# GPS Toll-based System Simulation

This is a Streamlit application that simulates a GPS toll-based system. The application allows users to select a vehicle type, start location, and end location, and then calculates the toll based on the distance traveled and the toll zones passed.

## Features

- Simulates vehicle movement between start and end locations.
- Calculates the toll based on vehicle type and toll zones.
- Displays the route and toll zones on a map using Folium.
- Supports different vehicle types including cars, trucks, bikes, buses, and ambulances.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Requirements

Below are the required dependencies for this project, which should be included in the `requirements.txt` file:

```
streamlit
simpy
geopandas
geopy
pandas
shapely
folium
```

## Usage

1. Select the vehicle type from the dropdown menu.
2. Choose the start and end locations.
3. Click on the "Calculate Toll" button to calculate the toll.
4. The app will display the total toll, distance, toll zones passed, and a map showing the route.
