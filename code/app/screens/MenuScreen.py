import services.Database as DB
import entities.StandardUser as SU
import entities.Admin as AD
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from screens.StatisticScreen import StatisticScreen

import requests
from services.Map import Map as MapWidget
from services.Pin import Pin
from screens.ManagmentScreen import ManagmentScreen
from screens.DetailsScreen import DetailsScreen
from entities.VehicleListing import VehicleListing


class MenuScreen(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user

        self.listings = [] 

        self.setWindowTitle("Admin Menu")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(1300, 800)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top menu layout
        top_menu_layout = QHBoxLayout()
        top_menu_layout.setAlignment(Qt.AlignLeft)

        # Logo
        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found at {logo_path}")
        logo_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        logo_label.setPixmap(pixmap.scaledToWidth(70, Qt.SmoothTransformation))
        logo_label.setCursor(Qt.PointingHandCursor)
        logo_label.mousePressEvent = self.reload_page
        top_menu_layout.addWidget(logo_label)

        # User icon
        admin_user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not admin_user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {admin_user_icon_path}")
        admin_user_label = QLabel()
        admin_user_pixmap = QPixmap(str(admin_user_icon_path))
        admin_user_label.setPixmap(admin_user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        admin_user_label.setCursor(Qt.PointingHandCursor)
        admin_user_label.mousePressEvent = self.do_nothing
        top_menu_layout.addWidget(admin_user_label)

        # Username label
        username_label = QLabel(f"Welcome, {self.admin_user.username}!")
        username_label.setStyleSheet("font-size: 14px; margin-left: 0px; color: white;")
        top_menu_layout.addWidget(username_label)

        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_menu_layout.addItem(spacer)

        # Logout button
        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #d9534f;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        logout_button.setCursor(Qt.PointingHandCursor)
        logout_button.clicked.connect(self.logout)
        top_menu_layout.addWidget(logout_button)

        # Top menu frame
        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")
        main_layout.addWidget(top_menu_frame)

        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Navigation menu
        nav_menu = QVBoxLayout()
        nav_menu.setAlignment(Qt.AlignTop)

        # Report Handling button
        report_button = QPushButton("Report Handling")
        report_button.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: white;
            text-align: left;
        """)
        report_button.clicked.connect(self.reportHandling)

        report_button_frame = QFrame()
        report_button_frame.setStyleSheet("border: 2px solid #ccc; padding: 5px; border-radius: 5px;")
        report_button_layout = QVBoxLayout()
        report_button_layout.addWidget(report_button)
        report_button_frame.setLayout(report_button_layout)
        nav_menu.addWidget(report_button_frame)

        # View Statistics button
        statistics_button = QPushButton("View Statistics")
        statistics_button.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: white;
            text-align: left;
        """)
        statistics_button.clicked.connect(self.displayStatisticScreen)

        statistics_button_frame = QFrame()
        statistics_button_frame.setStyleSheet("border: 2px solid #ccc; padding: 5px; border-radius: 5px;")
        statistics_button_layout = QVBoxLayout()
        statistics_button_layout.addWidget(statistics_button)
        statistics_button_frame.setLayout(statistics_button_layout)
        nav_menu.addWidget(statistics_button_frame)

        nav_menu.addStretch()

        nav_menu_frame = QFrame()
        nav_menu_frame.setLayout(nav_menu)
        nav_menu_frame.setFixedWidth(200)
        nav_menu_frame.setStyleSheet("background-color: skyblue;")
        content_layout.addWidget(nav_menu_frame)

        # Map Widget
        latitude, longitude = self.get_user_coordinates()
        self.map_widget = MapWidget(latitude=latitude, longitude=longitude)
        content_layout.addWidget(self.map_widget)

        # Fetch listings and place pins
        self.fetch_listings()
        self.place_pins()

        # Final layout
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def get_user_coordinates(self):
        return 38.246639, 21.734573  # Default to Patras center
        

    # fetch listings from the database
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

    # place pins on the map
    def place_pins(self):
        """Convert addresses to coordinates and place pins on the map."""
        for listing in self.listings:

            if listing.country and listing.city and listing.street and listing.number:
                address = f"{listing.street} {listing.number}, {listing.city}, {listing.country}"
                coords = self.get_coordinates_from_address_string(address)
                if coords:
                    pin = Pin(latitude=coords[0], longitude=coords[1], title=f"Listing ID: {listing.id}")
                    # Fix: lambda expects no arguments
                    pin.clicked.connect(lambda l_id=listing.id: self.open_details_screen(l_id))
                    self.map_widget.place(pin)

    # open details screen if clicked 
    def open_details_screen(self, listing_id):
        """Open the DetailsScreen window for the selected listing."""
        self.details_window = DetailsScreen(listing_id, user=self.admin_user)
        self.details_window.show()


    # convert address to coordinates using geocoding API
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


    # reload the page when logo is clicked
    def reload_page(self, event):
        self.close()
        self.__init__(self.admin_user)
        self.show()

    # logout and go back to login page
    def logout(self):
        from screens.LoginPage import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()

    def do_nothing(self, event):
        pass

    # open report handling screen
    def reportHandling(self):
        print("Report Handling is clicked!")
        self.admin_window = ManagmentScreen(AD.Admin(self.admin_user.username))
        self.admin_window.show()
        self.close()
    
    # open statistics screen    
    def displayStatisticScreen(self):
        print("View Statistics is clicked!")
        self.admin_window = StatisticScreen(AD.Admin(self.admin_user.username))
        self.admin_window.show()
        self.close()


