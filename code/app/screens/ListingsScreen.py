from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QScrollArea, QComboBox, QLineEdit, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
import mysql.connector
from screens.ListingScreen import ListingScreen  

class ListingsScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Listings Screen")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.map_screen = None
        self.showMaximized()

        main_layout = QVBoxLayout()

        # Top layout (for back button and header)
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

        # Filter toolbar layout
        filter_layout = QHBoxLayout()

        # Price filter
        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("Price per day")
        filter_layout.addWidget(self.price_input)

        # Vehicle type filter
        self.vehicle_type_combo = QComboBox(self)
        self.vehicle_type_combo.addItem("Any")
        self.vehicle_type_combo.addItem("Car")
        self.vehicle_type_combo.addItem("Truck")
        self.vehicle_type_combo.addItem("Motorbike")
        filter_layout.addWidget(self.vehicle_type_combo)

        # Brand filter
        self.brand_input = QLineEdit(self)
        self.brand_input.setPlaceholderText("Brand")
        filter_layout.addWidget(self.brand_input)

        # Fuel type filter
        self.fuel_type_combo = QComboBox(self)
        self.fuel_type_combo.addItem("Any")
        self.fuel_type_combo.addItem("Gasoline")
        self.fuel_type_combo.addItem("Diesel")
        self.fuel_type_combo.addItem("Electric")
        filter_layout.addWidget(self.fuel_type_combo)

        
        # Apply filter button
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

        # Reset filter button
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

        # Listings layout (the actual listings)
        self.listings_layout = QVBoxLayout()
        self.update_listings()  # Initial data fetch

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.listings_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def update_listings(self, listings=None):
        # If no listings are passed, fetch them from the DB
        if listings is None:
            listings = self.fetch_listings_from_db()

        # Clear current listings
        for i in range(self.listings_layout.count()):
            widget = self.listings_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not listings:
            no_listings_label = QLabel("No listings found.")
            no_listings_label.setStyleSheet("""
                font-size: 18px;
                color: #999;
                text-align: center;
                margin-top: 50px;
            """)
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
        # Reset all filter fields to their default state
        self.price_input.clear()
        self.vehicle_type_combo.setCurrentIndex(0)  # "Any"
        self.brand_input.clear()
        self.fuel_type_combo.setCurrentIndex(0)  # "Any"
        

        # Update listings without filters
        self.update_listings()

    def fetch_listings_from_db(self, filters=None):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="car_rental"
            )
            cursor = conn.cursor(dictionary=True)

            # Ξεκινάμε με ένα βασικό query
            query = "SELECT * FROM vehicle_listing WHERE 1"
            params = []

            # Ελέγχουμε και προσθέτουμε τα φίλτρα αν υπάρχουν
            if filters:
                # Φίλτρο τιμής ανά ημέρα (price_per_day)
                if filters["price_per_day"]:
                    try:
                        price = float(filters["price_per_day"])  # Βεβαιωνόμαστε ότι είναι έγκυρος αριθμός
                        query += " AND price_per_day <= %s"
                        params.append(price)
                    except ValueError:
                        print("Invalid price input")
                
                # Φίλτρο τύπου οχήματος (vehicle_type)
                if filters["vehicle_type"] != "Any":
                    query += " AND vehicle_type = %s"
                    params.append(filters["vehicle_type"])
                
                # Φίλτρο μάρκας (brand)
                if filters["brand"]:
                    query += " AND brand LIKE %s"
                    params.append(f"%{filters['brand']}%")
                
                # Φίλτρο τύπου καυσίμου (fuel_type)
                if filters["fuel_type"] != "Any":
                    query += " AND fuel_type = %s"
                    params.append(filters["fuel_type"])

            # Εκτέλεση της query με τα params
            cursor.execute(query, params)
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

    def back_to_map(self):
        from screens.MapScreen import MapScreen  # Lazy import to avoid circular import
        if self.map_screen is None:
            self.map_screen = MapScreen(self.user)
        self.map_screen.show()
        self.close()
