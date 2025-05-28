# GPS Toll-based System Simulation

This is a Streamlit application that simulates a GPS toll-based system. The application allows users to select a vehicle type, start location, and end location, and then calculates the toll based on the distance traveled and the toll zones passed.

## Features

- Simulates vehicle movement between start and end locations.
- Calculates the toll based on vehicle type and toll zones.
- Displays the route and toll zones on a map using Folium.
- Supports different vehicle types including cars, trucks, bikes, buses, and ambulances.

## Screenshots
![Screenshot 2025-05-28 111715](https://github.com/user-attachments/assets/1b10dfcb-2fb4-4110-88f9-ac713f68d1be)
![Screenshot 2025-05-28 111724](https://github.com/user-attachments/assets/45aaf04f-b3af-4e02-9382-1bdc77a66c31)
![Screenshot 2025-05-28 111734](https://github.com/user-attachments/assets/ecb9b740-5d5b-44c6-8869-40e8a5c6644a)
![Screenshot 2025-05-28 111749](https://github.com/user-attachments/assets/91236116-5ded-4145-b047-4ee85d1ad343)
![Screenshot 2025-05-28 111755](https://github.com/user-attachments/assets/2dd87f69-3fcb-431f-b56b-2d896e0a7f52)

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

## Usage

1. Select the vehicle type from the dropdown menu.
2. Choose the start and end locations.
3. Click on the "Calculate Toll" button to calculate the toll.
4. The app will display the total toll, distance, toll zones passed, and a map showing the route.
