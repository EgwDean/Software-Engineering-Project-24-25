import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QScrollArea,
    QComboBox, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from pathlib import Path
from services.Database import Database as DB
from screens.ListingScreen import ListingScreen

class ListingsScreen(QWidget):
    def __init__(self, user, map_screen=None):
        super().__init__()
        self.user = user
        self.setWindowTitle("Listings Screen")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.map_screen = map_screen  # Διατηρούμε την αναφορά στο MapScreen
        self.showMaximized()

        # Αντί για hardcoded paths, χρησιμοποιούμε το Path για τη σωστή διαχείριση
        self.assets_dir = Path(__file__).parent.parent.parent / 'assets' / 'images'

        main_layout = QVBoxLayout()

        # Top layout
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)

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

        header_label = QLabel("All Listings")
        header_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #007BFF;
            margin-left: 50px;
        """)
        top_layout.addWidget(header_label)

        main_layout.addLayout(top_layout)

        # Filter layout
        filter_layout = QHBoxLayout()

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price per day")
        filter_layout.addWidget(self.price_input)

        self.vehicle_type_combo = QComboBox()
        self.vehicle_type_combo.addItems(["Any", "Car", "Truck", "Motorbike"])
        filter_layout.addWidget(self.vehicle_type_combo)

        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Brand")
        filter_layout.addWidget(self.brand_input)

        self.fuel_type_combo = QComboBox()
        self.fuel_type_combo.addItems(["Any", "Gasoline", "Diesel", "Electric"])
        filter_layout.addWidget(self.fuel_type_combo)

        apply_filter_button = QPushButton("Apply Filters")
        apply_filter_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        apply_filter_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(apply_filter_button)

        reset_filter_button = QPushButton("Reset Filters")
        reset_filter_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #dc3545;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        reset_filter_button.clicked.connect(self.reset_filters)
        filter_layout.addWidget(reset_filter_button)

        main_layout.addLayout(filter_layout)

        # Listings section
        self.listings_layout = QVBoxLayout()
        self.update_listings()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.listings_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def update_listings(self, listings=None):
        if listings is None:
            listings = self.fetch_listings_from_db()

        for i in reversed(range(self.listings_layout.count())):
            widget = self.listings_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not listings:
            no_listings_label = QLabel("No listings found.")
            no_listings_label.setStyleSheet("font-size: 18px; color: #999; margin-top: 50px;")
            self.listings_layout.addWidget(no_listings_label)
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

                # Εικόνα
                image_label = QLabel()
                image_files = sorted(self.assets_dir.glob(f"img_{listing['id']}_*.jpg"))
                if image_files:
                    pixmap = QPixmap(str(image_files[0]))  # Πρώτη εικόνα της λίστας
                    pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("[Image not found]")

                image_label.setStyleSheet("margin-bottom: 10px;")
                listing_layout.addWidget(image_label)

                # Τίτλος
                title_label = QLabel(f"{listing['brand']} {listing['model']} ({listing['year']})")
                title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
                listing_layout.addWidget(title_label)

                # Περιγραφή
                description_label = QLabel(listing["description"])
                description_label.setStyleSheet("font-size: 14px; color: #666;")
                listing_layout.addWidget(description_label)

                # Τιμή
                price_label = QLabel(f"€{listing['price_per_day']} / day")
                price_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745;")
                listing_layout.addWidget(price_label)

                # View More
                view_more_button = QPushButton("View More")
                view_more_button.setStyleSheet("""
                    padding: 10px 20px;
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    font-size: 14px;
                """)
                view_more_button.clicked.connect(lambda _, l=listing: self.open_listing_screen(l))
                listing_layout.addWidget(view_more_button)

                listing_frame.setLayout(listing_layout)
                self.listings_layout.addWidget(listing_frame)

    def apply_filters(self):
        filters = {
            "price_per_day": self.price_input.text(),
            "vehicle_type": self.vehicle_type_combo.currentText(),
            "brand": self.brand_input.text(),
            "fuel_type": self.fuel_type_combo.currentText(),
        }
        listings = self.fetch_listings_from_db(filters)
        self.update_listings(listings)

    def reset_filters(self):
        self.price_input.clear()
        self.vehicle_type_combo.setCurrentIndex(0)
        self.brand_input.clear()
        self.fuel_type_combo.setCurrentIndex(0)
        self.update_listings()

    def fetch_listings_from_db(self, filters=None):
        conn = DB.connect()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM vehicle_listing WHERE 1 AND name_of_user != %s"
        params = [self.user.username]

        if filters:
            if filters["price_per_day"]:
                try:
                    price = float(filters["price_per_day"])
                    query += " AND price_per_day <= %s"
                    params.append(price)
                except ValueError:
                    print("Invalid price input")

            if filters["vehicle_type"] != "Any":
                query += " AND vehicle_type = %s"
                params.append(filters["vehicle_type"])

            if filters["brand"]:
                query += " AND brand LIKE %s"
                params.append(f"%{filters['brand']}%")

            if filters["fuel_type"] != "Any":
                query += " AND fuel_type = %s"
                params.append(filters["fuel_type"])

        cursor.execute(query, params)
        listings = cursor.fetchall()

        cursor.close()
        conn.close()

        return listings

    def open_listing_screen(self, listing_data):
        self.listing_screen = ListingScreen(self.user, listing_data)
        self.listing_screen.show()

    def back_to_map(self):
        # Απλώς κλείνουμε την ListingsScreen
        self.close()