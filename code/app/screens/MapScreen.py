from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from pathlib import Path
import requests
from services.Map import MapWidget
from services.Pin import Pin
from entities.VehicleListing import VehicleListing
import services.Database as DB


class MapScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.listings = []  # Store all VehicleListing instances
        self.setWindowTitle("Map Screen")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.showMaximized()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === Top menu ===
        top_menu_layout = QHBoxLayout()
        top_menu_layout.setAlignment(Qt.AlignLeft)

        # Logo
        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found at {logo_path}")
        logo_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        logo_label.setPixmap(pixmap.scaledToWidth(70, Qt.SmoothTransformation))
        top_menu_layout.addWidget(logo_label)

        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_bar.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: none;
            background-color: white;
            border-radius: 5px;
        """)
        top_menu_layout.addWidget(search_bar)

        # Filter icon
        filter_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-filter-30.png'
        if not filter_icon_path.exists():
            raise FileNotFoundError(f"Filter icon file not found at {filter_icon_path}")
        filter_label = QLabel()
        filter_pixmap = QPixmap(str(filter_icon_path))
        filter_label.setPixmap(filter_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        top_menu_layout.addWidget(filter_label)

        # User icon
        user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {user_icon_path}")
        user_label = QLabel()
        user_pixmap = QPixmap(str(user_icon_path))
        user_label.setPixmap(user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        top_menu_layout.addWidget(user_label)

        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")
        main_layout.addWidget(top_menu_frame)

        # === Content layout ===
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Navigation menu
        nav_menu = QVBoxLayout()
        nav_menu.setAlignment(Qt.AlignTop)

        for i in range(5):
            button = QPushButton(f"TODO {i + 1}")
            button.setStyleSheet("""
                padding: 10px;
                font-size: 14px;
                background-color: skyblue;
                border: none;
                color: white;
                text-align: left;
            """)
            nav_menu.addWidget(button)

        nav_menu.addStretch()

        nav_menu_frame = QFrame()
        nav_menu_frame.setLayout(nav_menu)
        nav_menu_frame.setFixedWidth(200)
        nav_menu_frame.setStyleSheet("background-color: skyblue;")
        content_layout.addWidget(nav_menu_frame)

        # Map widget
        user_coords = self.get_user_coordinates()
        self.map_widget = MapWidget(latitude=user_coords[0], longitude=user_coords[1])
        content_layout.addWidget(self.map_widget)

        # Fetch listings and place pins
        self.fetch_listings()
        self.place_pins()

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def get_user_coordinates(self):
        """Fetch the user's address and convert it to coordinates."""
        try:
            db = DB.Database()
            connection = db.connect()

            if connection is None:
                print("Failed to connect to the database.")
                return 51.505, -0.09  # Default to London

            cursor = connection.cursor()
            query = """
                SELECT country, city, street, number
                FROM address
                WHERE username_address = %s
            """
            cursor.execute(query, (self.user.username,))
            result = cursor.fetchone()

            if result:
                country, city, street, number = result
                address = f"{street} {number}, {city}, {country}"
                coords = self.get_coordinates_from_address_string(address)
                if coords:
                    return coords

            cursor.close()
            connection.close()

        except Exception as e:
            print(f"An error occurred while fetching user coordinates: {e}")

        return 51.505, -0.09  # Default to London

    def fetch_listings(self):
        """Fetch all listings from the database and create VehicleListing instances."""
        try:
            db = DB.Database()
            connection = db.connect()

            if connection is None:
                print("Failed to connect to the database.")
                return

            cursor = connection.cursor()
            query = "SELECT id FROM vehicle_listing"
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                listing_id = row[0]
                listing = VehicleListing(listing_id)
                self.listings.append(listing)

            cursor.close()
            connection.close()

            print(f"Fetched {len(self.listings)} listings from the database.")

        except Exception as e:
            print(f"An error occurred while fetching listings: {e}")

    def place_pins(self):
        """Convert addresses to coordinates and place pins on the map."""
        for listing in self.listings:
            if listing.country and listing.city and listing.street and listing.number:
                address = f"{listing.street} {listing.number}, {listing.city}, {listing.country}"
                coords = self.get_coordinates_from_address_string(address)
                if coords:
                    pin = Pin(latitude=coords[0], longitude=coords[1], title=f"Listing ID: {listing.id}")
                    self.map_widget.place(pin)

    def get_coordinates_from_address_string(self, address):
        """Convert an address string to latitude and longitude using a geocoding API."""
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": address, "format": "json"}
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

    def do_nothing(self, event):
        """Placeholder for unimplemented functionality."""
        pass