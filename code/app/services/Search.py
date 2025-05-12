import requests

class Search:
    def __init__(self, map_widget):
        """
        Initialize the Search class with a reference to the map widget.
        :param map_widget: The MapWidget instance to update the map's center.
        """
        self.map_widget = map_widget

    def search(self, location):
        """
        Search for a location and center the map on it.
        :param location: The location string to search for.
        """
        try:
            coords = self.get_coordinates_from_location(location)
            if coords:
                self.map_widget.setCenter(coords[0], coords[1])  # Center the map
                print(f"Map centered on: {location} ({coords[0]}, {coords[1]})")
            else:
                print(f"Could not find coordinates for location: {location}")
        except Exception as e:
            print(f"An error occurred during the search: {e}")

    def get_coordinates_from_location(self, location):
        """
        Convert a location string to latitude and longitude using a geocoding API.
        :param location: The location string to geocode.
        :return: A tuple of (latitude, longitude) or None if not found.
        """
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": location, "format": "json"}
            headers = {"User-Agent": "PyQtMapApp"}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return lat, lon
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None