import pytest
from project import fetch_locations  # Import the function

@pytest.mark.integration
def test_fetch_valid_city_state():
    """Test fetching coordinates for a valid city and state."""
    locations = ["New York, NY"]
    results = fetch_locations(locations)

    assert isinstance(results, list) and len(results) > 0, "Result should be a list with at least one item"
    assert "latitude" in results[0] and "longitude" in results[0], "Missing coordinates"
    assert "place_name" in results[0], "Missing place name"
