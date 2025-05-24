import sys
import requests
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFrame, QToolButton, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon

import services.Database as DB
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
        self.listings = []
        self.setWindowTitle("Map Screen")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.showMaximized()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self._init_top_menu()
        self._init_content_layout()

        self.setLayout(self.main_layout)

        # self.search = Search(self.map_widget)

    def _init_top_menu(self):
        top_menu_layout = QHBoxLayout()
        top_menu_layout.setAlignment(Qt.AlignLeft)

        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(str(logo_path)).scaledToWidth(70, Qt.SmoothTransformation))
        top_menu_layout.addWidget(logo_label)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("padding: 8px; font-size: 14px; background-color: white; border-radius: 5px;")
        self.search_bar.returnPressed.connect(self.perform_search)
        top_menu_layout.addWidget(self.search_bar)

        search_icon = Path(__file__).parent.parent.parent / 'assets' / 'icons8-search-30.png'
        search_button = QToolButton()
        search_button.setIcon(QIcon(str(search_icon)))
        search_button.setStyleSheet("border: none; background-color: transparent;")
        search_button.clicked.connect(self.perform_search)
        top_menu_layout.addWidget(search_button)

        filter_icon = Path(__file__).parent.parent.parent / 'assets' / 'icons8-filter-30.png'
        filter_button = QToolButton()
        filter_button.setIcon(QIcon(str(filter_icon)))
        filter_button.setStyleSheet("border: none; background-color: transparent;")
        filter_button.clicked.connect(self.open_filter_popup)
        top_menu_layout.addWidget(filter_button)

        clear_filters_button = QPushButton("Clear Filters")
        clear_filters_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: skyblue; border: 1px solid black; border-radius: 5px;")
        clear_filters_button.clicked.connect(self.clear_filters)
        top_menu_layout.addWidget(clear_filters_button)

        user_icon = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        user_label = QLabel()
        user_label.setPixmap(QPixmap(str(user_icon)).scaledToWidth(30, Qt.SmoothTransformation))
        user_label.setCursor(Qt.PointingHandCursor)
        user_label.mousePressEvent = self.open_profile_screen
        top_menu_layout.addWidget(user_label)

        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")
        self.main_layout.addWidget(top_menu_frame)

    def _init_content_layout(self):
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)

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

        # Add any remaining TODO buttons if needed
        for i in range(2):
            button = QPushButton(f"TODO {i + 3}")
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
        nav_frame = QFrame()
        nav_frame.setLayout(nav_menu)
        nav_frame.setFixedWidth(200)
        nav_frame.setStyleSheet("background-color: skyblue;")
        self.content_layout.addWidget(nav_frame)

        user_coords = self.get_user_coordinates()
        self.map_widget = Map(latitude=user_coords[0], longitude=user_coords[1])
        self.map_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.map_widget, stretch=1)

        self.main_layout.addLayout(self.content_layout)

        self.fetch_listings()
        self.place_pins()

        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)

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
        try:
            db = DB.Database()
            conn = db.connect()
            if conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM vehicle_listing WHERE status='listed'")
                for (listing_id,) in cur.fetchall():
                    listing = VehicleListing(listing_id)
                    self.listings.append(listing)
                cur.close()
                conn.close()
        except Exception as e:
            print(f"Error fetching listings: {e}")

    def place_pins(self):
        for listing in self.listings:
            if listing.name_of_user == self.user.username:
                continue
            if listing.country and listing.city and listing.street and listing.number:
                address = f"{listing.street} {listing.number}, {listing.city}, {listing.country}"
                coords = self.get_coordinates_from_address_string(address)
                if coords:
                    pin = Pin(latitude=coords[0], longitude=coords[1], title=f"Listing ID: {listing.id}")
                    pin.clicked.connect(lambda _, lid=listing.id: self.open_details_screen(lid))
                    self.map_widget.place(pin)

    def open_details_screen(self, listing_id):
        self.details_window = DetailsScreen(listing_id, user=self.user)
        self.details_window.show()

    def open_history(self):
        """Instantiate and show the HistoryPage."""
        self.history_page = HistoryPage(self.user)
        self.history_page.back_requested.connect(self.show)
        self.hide()
        self.history_page.show()

    def _on_history_back(self):
        self.history_page.close()
        self.show()
        self.raise_()
        self.showMaximized()

        # ✅ Force layout update and repaint
        self.layout().activate()
        self.map_widget.updateGeometry()
        QTimer.singleShot(0, lambda: self.map_widget.resize(self.content_layout.geometry().size()))
        self.map_widget.repaint()

    def open_listings(self):
        self.listings_window = ListingsScreen(self.user)
        self.listings_window.show()

    def open_profile_screen(self, event=None):
        from screens.ProfileScreen import ProfileScreen
        self.profile_screen = ProfileScreen(self.user, self)
        self.profile_screen.show()

    def get_user_coordinates(self):
        try:
            db = DB.Database()
            conn = db.connect()
            if conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT country, city, street, number FROM address WHERE username_address=%s",
                    (self.user.username,)
                )
                r = cur.fetchone()
                cur.close()
                conn.close()
                if r:
                    country, city, street, number = r
                    address = f"{street} {number}, {city}, {country}"
                    coords = self.get_coordinates_from_address_string(address)
                    if coords:
                        return coords
        except Exception as e:
            print(f"Error in get_user_coordinates: {e}")
        return 51.505, -0.09

    def open_create_screen(self):
        from screens.CreateScreen import CreateScreen
        self.create_screen = CreateScreen(self.user)
        self.create_screen.show()

    def get_coordinates_from_address_string(self, address):
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": address, "format": "json"}
            headers = {"User-Agent": "PyQtMapApp"}
            resp = requests.get(url, params=params, headers=headers)
            data = resp.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None

    def perform_search(self):
        loc = self.search_bar.text().strip()
        if loc:
            coords = self.get_coordinates_from_address_string(loc)
            if coords:
                self.map_widget.center_map(coords[0], coords[1])

    def open_filter_popup(self):
        dlg = Filter(self.map_widget, self)
        dlg.exec_()

    def clear_filters(self):
        self.listings.clear()
        self.fetch_listings()
        self.map_widget.clear_pins()
        self.place_pins()
