import requests
import tkinter as tk
from typing import List, Dict, Union
from dotenv import load_dotenv
import os 

load_dotenv()

API_KEY = os.getenv("GEO_API_KEY")
if not API_KEY:
    raise ValueError("API Key is missing!")

BASE_URL = "http://api.openweathermap.org/geo/1.0/"

def get_coordinates_by_location(city: str, state: str = "", country: str = "US") -> Dict[str, Union[str, float]]:
    """
    Fetch latitude and longitude using city and state.
    """
    query = f"{city},{state},{country}" if state else f"{city},{country}"
    url = f"{BASE_URL}direct?q={query}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data:
        location = data[0]  # Take the first result
        return {
            "place_name": f"{location.get('name')}, {state if state else location.get('state', '')}, {country}",
            "latitude": location.get("lat"),
            "longitude": location.get("lon"),
        }
    return {"error": "Location not found or invalid response."}

def get_coordinates_by_zip(zip_code: str, country: str = "US") -> Dict[str, Union[str, float]]:
    """
    Fetch latitude and longitude using ZIP code.
    """
    url = f"{BASE_URL}zip?zip={zip_code},{country}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "lat" in data and "lon" in data:
        return {
            "place_name": f"{data.get('name')}, {country}",
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
        }
    return {"error": "ZIP code not found or invalid response."}

def fetch_locations(locations: List[str]) -> List[Dict[str, Union[str, float]]]:
    """
    Fetch geolocation data for multiple locations (city/state or zip code).
    """
    results = []
    for location in locations:
        if location.isdigit():  # Check if input is a ZIP code
            result = get_coordinates_by_zip(location)
        else:
            city_state = location.split(",")
            city = city_state[0].strip()
            state = city_state[1].strip() if len(city_state) > 1 else ""
            result = get_coordinates_by_location(city, state)
        results.append(result)
    return results

def fetch_and_display():
    locations = entry.get().split(";")
    results = fetch_locations([loc.strip() for loc in locations])
    output_text.delete("1.0", tk.END)
    for res in results:
        output_text.insert(tk.END, f"{res}\n\n")

# UI Setup (Only runs if executed directly)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Geolocation Finder")
    root.geometry("500x400")

    tk.Label(root, text="Enter locations (comma-separated city,state or ZIP, separated by ';'):").pack(pady=5)
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)

    tk.Button(root, text="Fetch Coordinates", command=fetch_and_display).pack(pady=5)

    output_text = tk.Text(root, height=15, width=60)
    output_text.pack(pady=5)

    root.mainloop()
