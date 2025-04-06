import streamlit as st
import geopy.distance
import webbrowser

# Predefined airports data
airports = [
    {"name": "Valencia Airport", "code": "VLC", "city": "Valencia", "country": "Spain", "lat": 39.4893, "lon": -0.4816, "plane": "Ilyushin Il-76"},
    {"name": "Castellón Airport", "code": "CDT", "city": "Castellón", "country": "Spain", "lat": 40.2139, "lon": 0.0733, "plane": "ATR 72"},
    # Add other airports here as needed
]

# Function to calculate distance
def calculate_distance(city_lat, city_lon, airport_lat, airport_lon):
    coords_1 = (city_lat, city_lon)
    coords_2 = (airport_lat, airport_lon)
    return geopy.distance.distance(coords_1, coords_2).km

# Streamlit UI
st.title('Planespotting Airport Finder')

# User inputs
city = st.text_input("Enter your city:")
country = st.text_input("Enter your country:")

# Function to find the best airport
def find_best_airport(city, country):
    if not city or not country:
        st.error("Please provide both city and country!")
        return

    # For simplicity, we assume city/country are in a dictionary with lat/lon data
    # You can expand it with a more complete geolocation service
    city_coords = {
        "almenara,spain": (39.7686, -0.2287),  # example coordinates for Almenara, Spain
        "valencia,spain": (39.4699, -0.3763),
        # Add more city coordinates here
    }
    
    # Get coordinates for the entered city and country
    key = f"{city.lower()},{country.lower()}"
    if key not in city_coords:
        st.error("City not found in our database.")
        return
    
    city_lat, city_lon = city_coords[key]
    
    closest_airport = None
    closest_distance = float('inf')
    
    # Find the closest airport
    for airport in airports:
        distance = calculate_distance(city_lat, city_lon, airport["lat"], airport["lon"])
        if distance < closest_distance:
            closest_distance = distance
            closest_airport = airport
    
    if closest_airport:
        st.subheader(f"Closest Airport: {closest_airport['name']} ({closest_airport['code']})")
        st.write(f"Distance: {closest_distance:.2f} km")
        st.write(f"Rarest commonly seen plane: {closest_airport['plane']}")
        
        # Google Maps link
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={city_lat},{city_lon}&destination={closest_airport['lat']},{closest_airport['lon']}"
        st.markdown(f"[Click here for Google Maps directions]( {maps_url} )")
    else:
        st.error("No airport found.")

# Button to trigger the search
if st.button("Find Best Airport"):
    find_best_airport(city, country)
