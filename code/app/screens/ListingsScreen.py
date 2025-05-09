from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt
import mysql.connector
from screens.ListingScreen import ListingScreen  # Για το "View More"

class ListingsScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Listings Screen")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.map_screen = None
        self.showMaximized()

        main_layout = QVBoxLayout()

        # Top layout
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)

        # Back button
        back_button = QPushButton("Back to Map")
        back_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #007BFF;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        back_button.clicked.connect(self.back_to_map)
        top_layout.addWidget(back_button)

        # Header
        header_label = QLabel("All Listings")
        header_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #007BFF;
            margin-left: 50px;
        """)
        top_layout.addWidget(header_label)

        main_layout.addLayout(top_layout)

        # Listings layout
        listings_layout = QVBoxLayout()
        listings = self.fetch_listings_from_db()

        if not listings:
            no_listings_label = QLabel("No listings found.")
            no_listings_label.setStyleSheet("""
                font-size: 18px;
                color: #999;
                text-align: center;
                margin-top: 50px;
            """)
            listings_layout.addWidget(no_listings_label)
        else:
            for listing in listings:
                listing_frame = QFrame()
                listing_frame.setStyleSheet("""
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    padding: 15px;
                """)
                listing_layout = QVBoxLayout()

                title_label = QLabel(f"{listing['brand']} {listing['model']} ({listing['year']})")
                title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
                listing_layout.addWidget(title_label)

                description_label = QLabel(listing["description"])
                description_label.setStyleSheet("font-size: 14px; color: #666;")
                listing_layout.addWidget(description_label)

                price_label = QLabel(f"€{listing['price_per_day']} / day")
                price_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745;")
                listing_layout.addWidget(price_label)

                # View More Button
                view_more_button = QPushButton("View More")
                view_more_button.setStyleSheet("""
                    padding: 10px 20px;
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    font-size: 14px;
                """)

                # Χρήση lambda για να περάσουμε σωστά το συγκεκριμένο listing
                view_more_button.clicked.connect(lambda _, l=listing: self.open_listing_screen(l))
                listing_layout.addWidget(view_more_button)

                listing_frame.setLayout(listing_layout)
                listings_layout.addWidget(listing_frame)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(listings_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def fetch_listings_from_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="car_rental"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vehicle_listing")
            listings = cursor.fetchall()
            cursor.close()
            conn.close()
            return listings
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def open_listing_screen(self, listing_data):
        self.listing_screen = ListingScreen(self.user, listing_data)
        self.listing_screen.show()
        self.close()

    def back_to_map(self):
        from screens.MapScreen import MapScreen  # Lazy import to avoid circular import
        if self.map_screen is None:
            self.map_screen = MapScreen(self.user)
        self.map_screen.show()
        self.close()
