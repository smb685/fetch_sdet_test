import requests #<- used for making http requests to fetch data 
import tkinter as tk # <- this is the possible GUI toolkit to create a simple interface 
from typing import List, Dict, Union  # <- provies type hints for functions parameteres and returns values
from dotenv import load_dotenv # <-loads the enviroment variable from .env file
import os 

load_dotenv()  # <- this function loaded variables from the .env file into the program and it helps store the API keys. securly prevents me from harcoding it in. 

API_KEY = os.getenv("GEO_API_KEY")    # os.getenv("GEO_API_KEY") ; grabs the api key from the enviorment 
if not API_KEY:
    raise ValueError("API Key is missing!")  # in the event the key is missing, the error defined will popoulate 


BASE_URL = "http://api.openweathermap.org/geo/1.0/" # <- this is just the base url from openweathermap's api

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
    results = []  # Initialize an empty list to store the results for each location.
    for location in locations:  # Loop through each location in the input list 'locations'.
        if location.isdigit():  # Check if the current location is a ZIP code by checking if it's made up of digits.
            result = get_coordinates_by_zip(location)  # If it is a ZIP code, call the function to get coordinates by ZIP.
        else:   # If the location is not a ZIP code (i.e., it's in "city, state" format).
            city_state = location.split(",")  # Split the location into city and state based on the comma separator.
            city = city_state[0].strip()  # Assign the first part (city) to the variable 'city', removing leading/trailing spaces.
            state = city_state[1].strip() if len(city_state) > 1 else ""  # Assign the second part (state) to 'state', or an empty string if no state is present.
            result = get_coordinates_by_location(city, state)  # Fetch coordinates using the city and state (or empty string for state).
        results.append(result) # Add a single result location to the results list.
    return results # After processing all locations, return the list of results.

def fetch_and_display(): #This function retrieves user input from the entry field, processes it, and displays the results in the text box.
    locations = entry.get().split(";") #  This retrieves the text entered by the user in the entry field and splits it at each semicolon (;).
    results = fetch_locations([loc.strip() for loc in locations]) #This calls the fetch_locations() function with a cleaned list of locations.
    output_text.delete("1.0", tk.END) # This clears the Text widget before displaying new results
    for res in results: #This starts a loop over the results returned from
        output_text.insert(tk.END, f"{res}\n\n") #This inserts each result into the Text widget, adding two new lines (\n\n) after each entry for spacing.

# UI Setup (Only runs if executed directly)
if __name__ == "__main__": #This ensures the following code runs only when the script is executed directly, not when imported as a module.
    root = tk.Tk() #This creates the main window (root) using Tkinter.
    root.title("Geolocation Finder") #This sets the window title to "Geolocation Finder"
    root.geometry("500x400") #This sets the window size to 500 pixels wide and 400 pixels tall.

    tk.Label(root, text="Enter locations (comma-separated city,state or ZIP, separated by ';'):").pack(pady=5) #This creates a label at the top of the window with user instructions. .pack(pady=5): Adds vertical padding (5 pixels) above and below the label.
    entry = tk.Entry(root, width=50) #This creates a text input field (entry) where the user can enter locations. 50 character limit 
    entry.pack(pady=5) #adds padding

    tk.Button(root, text="Fetch Coordinates", command=fetch_and_display).pack(pady=5) #This creates a button labeled "Fetch Coordinates". When the button is clicked, it calls fetch_and_display().

    output_text = tk.Text(root, height=15, width=60) #This creates a Text widget to display the fetched results.
    output_text.pack(pady=5) #

    root.mainloop() #This starts the Tkinter event loop, keeping the window open and waiting for user input.
