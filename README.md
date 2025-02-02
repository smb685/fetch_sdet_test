# FETCH_SDET_TEST

## Overview
FETCH_SDET_TEST is a Python-based application that retrieves geographical coordinates (latitude and longitude) using OpenWeatherMap's Geolocation API. The application supports fetching coordinates using either city/state or ZIP codes and features a simple graphical user interface (GUI) built with Tkinter.

## Features
- Retrieve latitude and longitude using city/state or ZIP codes.
- Secure API key handling with `.env` file.
- Graphical user interface (GUI) for easy interaction.
- Integration tests to ensure API functionality.

## Installation
### Prerequisites
Ensure you have Python installed (version 3.7 or higher recommended). You will also need to install the following dependencies:

```bash
pip install requests python-dotenv pytest tkinter
```

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/smb685/fetch_sdet_test.git
   cd fetch_sdet_test
   ```
2. Create a `.env` file in the root directory and add your OpenWeatherMap API key:
   ```
   GEO_API_KEY=f897a99d971b5eef57be6fafa0d83239
   ```
3. Run the application:
   ```bash
   python project.py
   ```

## Usage


### Graphical Interface
1. Run the application:
   ```bash
   python3 project.py
   ```
2. Enter a city/state (e.g., `New York, NY`) or ZIP code (e.g., `10001`).
3. Click "Fetch Coordinates" to retrieve and display the location data.

## Testing
Integration tests are included to validate the API responses.
Run tests using:

```bash
pytest test_project.py
```

## Code Structure
- `project.py`: Main application file containing the functions to fetch geolocation data and the GUI implementation.
- `test_project.py`: Test file using `pytest` to verify API functionality.
- `.env`: Stores the API key securely (not included in version control).


## License
This project is licensed under the MIT License.

## Contact
For any inquiries, reach out to sylvestermbrandon3@gmail.com or on Github at https://github.com/smb685.

## Video 

![Untitled Video February 2, 2025 12_13 AM](https://github.com/user-attachments/assets/c91680ce-8fa1-4a3b-b5c4-e5b55248fd95)
