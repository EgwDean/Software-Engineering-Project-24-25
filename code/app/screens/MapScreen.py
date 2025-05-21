from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QToolButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from pathlib import Path
import requests
from services.Map import Map
from services.Pin import Pin
from entities.VehicleListing import VehicleListing
import services.Database as DB
from services.Filter import Filter 
from screens.DetailsScreen import DetailsScreen
from screens.HistoryPage import HistoryPage
from screens.ListingsScreen import ListingsScreen
from screens.CreateScreen import CreateScreen


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
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: none;
            background-color: white;
            border-radius: 5px;
        """)
        self.search_bar.returnPressed.connect(self.perform_search)
        top_menu_layout.addWidget(self.search_bar)

        # Search button with icon
        search_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-search-30.png'
        if not search_icon_path.exists():
            raise FileNotFoundError(f"Search icon file not found at {search_icon_path}")
        search_button = QToolButton()
        search_button.setIcon(QIcon(str(search_icon_path)))  # Wrap QPixmap in QIcon
        search_button.setStyleSheet("""
            border: none;
            background-color: transparent;
        """)
        search_button.clicked.connect(self.perform_search)
        top_menu_layout.addWidget(search_button)

        # Filter icon
        filter_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-filter-30.png'
        if not filter_icon_path.exists():
            raise FileNotFoundError(f"Filter icon file not found at {filter_icon_path}")
        filter_button = QToolButton()
        filter_button.setIcon(QIcon(str(filter_icon_path)))  # Wrap QPixmap in QIcon
        filter_button.setStyleSheet("""
            border: none;
            background-color: transparent;
        """)
        filter_button.clicked.connect(self.open_filter_popup)  # Connect to the filter popup
        top_menu_layout.addWidget(filter_button)

        # Clear Filters button
        clear_filters_button = QPushButton("Clear Filters")
        clear_filters_button.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            background-color: skyblue;
            border: 1px solid black;
            border-radius: 5px;
        """)
        clear_filters_button.clicked.connect(self.clear_filters)  # Connect to the clear_filters method
        top_menu_layout.addWidget(clear_filters_button)

        # User icon
        user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {user_icon_path}")
        user_label = QLabel()
        user_pixmap = QPixmap(str(user_icon_path))
        user_label.setPixmap(user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        user_label.setCursor(Qt.PointingHandCursor)
        user_label.mousePressEvent = self.open_profile_screen  # Link to ProfileScreen
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

        # View All Listings button
        view_all_btn = QPushButton("View All Listings")
        view_all_btn.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: black;
            text-align: left;
            border: 1px solid black;
        """)
        view_all_btn.clicked.connect(self.open_listings)
        nav_menu.addWidget(view_all_btn)

        # History button
        history_btn = QPushButton("History")
        history_btn.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: black;
            text-align: left;
            border: 1px solid black;
        """)
        history_btn.clicked.connect(self.open_history)
        nav_menu.addWidget(history_btn)

        # Create Listing button
        create_btn = QPushButton("Create Listing")
        create_btn.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: black;
            text-align: left;
            border: 1px solid black;
        """)
        create_btn.clicked.connect(self.open_create_screen)
        nav_menu.addWidget(create_btn)

        # Subscription button
        subscription_btn = QPushButton("Subscription")
        subscription_btn.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: black;
            text-align: left;
            border: 1px solid black;
        """)
        subscription_btn.clicked.connect(self.open_subscription_screen)
        nav_menu.addWidget(subscription_btn)

        # Add any remaining TODO buttons if needed
        for i in range(1):
            button = QPushButton(f"TODO {i + 4}")
            button.setStyleSheet("""
                padding: 10px;
                font-size: 14px;
                background-color: skyblue;
                border: none;
                color: black;
                text-align: left;
                border: 1px solid black;
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
        self.map_widget = Map(latitude=user_coords[0], longitude=user_coords[1])
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
            query = "SELECT id FROM vehicle_listing WHERE status = 'listed'"
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
            # Skip listings that belong to the logged-in user
            if listing.name_of_user == self.user.username:
                continue

            if listing.country and listing.city and listing.street and listing.number:
                address = f"{listing.street} {listing.number}, {listing.city}, {listing.country}"
                coords = self.get_coordinates_from_address_string(address)
                if coords:
                    pin = Pin(latitude=coords[0], longitude=coords[1], title=f"Listing ID: {listing.id}")
                    # Fix: lambda expects no arguments
                    pin.clicked.connect(lambda l_id=listing.id: self.open_details_screen(l_id))
                    self.map_widget.place(pin)

    def open_details_screen(self, listing_id):
        """Open the DetailsScreen window for the selected listing."""
        self.details_window = DetailsScreen(listing_id, user=self.user)
        self.details_window.show()

    def open_history(self):
        """Instantiate and show the HistoryPage."""
        self.history_page = HistoryPage(self.user)
        self.history_page.back_requested.connect(self.show)
        self.hide()
        self.history_page.show()

    def open_listings(self, event=None):
        # Create and show the ListingsScreen window
        self.listings_window = ListingsScreen(self.user)
        self.listings_window.show()

    def open_profile_screen(self, event=None):
        # Αναβολή της εισαγωγής της ProfileScreen εδώ
        from screens.ProfileScreen import ProfileScreen  # Εισάγουμε την ProfileScreen μόνο όταν χρειάζεται
        self.profile_screen = ProfileScreen(self.user, self)  # Δημιουργούμε την ProfileScreen
        self.profile_screen.show()  # Εμφανίζουμε την ProfileScreen

    def open_create_screen(self):
        from screens.CreateScreen import CreateScreen
        self.create_screen = CreateScreen(self.user)
        self.create_screen.show()

    def open_subscription_screen(self):
        from screens.SubscriptionScreen import SubscriptionScreen
        self.subscription_screen = SubscriptionScreen(self.user)
        self.subscription_screen.show()

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

    def perform_search(self):
        """Perform a search using the search bar and center the map."""
        location = self.search_bar.text().strip()
        if location:
            coords = self.get_coordinates_from_address_string(location)
            if coords:
                self.map_widget.center_map(coords[0], coords[1])
            else:
                print(f"Could not find coordinates for location: {location}")
        else:
            print("Search bar is empty. Please enter a location.")

    def open_filter_popup(self):
        """Open the filter popup."""
        print("Opening filter popup.")  # Debug
        filter_dialog = Filter(self.map_widget, self)
        filter_dialog.exec_()

    def clear_filters(self):
        """Clear all filters and reload the pins."""
        print("Clearing filters...")
        self.listings = []  # Reset listings
        self.fetch_listings()  # Re-fetch all listings
        self.map_widget.clear_pins()  # Clear existing pins on the map
        self.place_pins()  # Place all pins again
        print("Filters cleared and pins reloaded.")
