from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox
import services.Database as DB
from services.Pin import Pin
import requests

class Filter(QDialog):
    def __init__(self, map_widget, parent=None):
        super().__init__(parent)
        self.map_widget = map_widget
        self.setWindowTitle("Filter Listings")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Price per day range
        layout.addWidget(QLabel("Price per day range:"))
        self.min_price = QLineEdit()
        self.min_price.setPlaceholderText("Min price")
        self.max_price = QLineEdit()
        self.max_price.setPlaceholderText("Max price")
        price_layout = QHBoxLayout()
        price_layout.addWidget(self.min_price)
        price_layout.addWidget(self.max_price)
        layout.addLayout(price_layout)

        # Total km range
        layout.addWidget(QLabel("Total km range:"))
        self.min_km = QLineEdit()
        self.min_km.setPlaceholderText("Min km")
        self.max_km = QLineEdit()
        self.max_km.setPlaceholderText("Max km")
        km_layout = QHBoxLayout()
        km_layout.addWidget(self.min_km)
        km_layout.addWidget(self.max_km)
        layout.addLayout(km_layout)

        # Vehicle type, brand, and model
        self.vehicle_type = QComboBox()
        self.brand = QComboBox()
        self.model = QComboBox()
        layout.addWidget(QLabel("Vehicle Type:"))
        layout.addWidget(self.vehicle_type)
        layout.addWidget(QLabel("Brand:"))
        layout.addWidget(self.brand)
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model)

        # Populate dropdowns with data from the database
        self.populate_dropdowns()

        # Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_filters)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def populate_dropdowns(self):
        """Fetch unique values for vehicle type, brand, and model from the database."""
        try:
            db = DB.Database()
            connection = db.connect()
            if connection is None:
                print("Failed to connect to the database.")
                return

            cursor = connection.cursor()

            # Populate vehicle type
            self.vehicle_type.clear()
            self.vehicle_type.addItem("Any")
            cursor.execute("SELECT DISTINCT vehicle_type FROM vehicle_listing")
            self.vehicle_type.addItems([row[0] for row in cursor.fetchall()])

            # Populate brand
            self.brand.clear()
            self.brand.addItem("Any")
            cursor.execute("SELECT DISTINCT brand FROM vehicle_listing")
            self.brand.addItems([row[0] for row in cursor.fetchall()])

            # Populate model
            self.model.clear()
            self.model.addItem("Any")
            cursor.execute("SELECT DISTINCT model FROM vehicle_listing")
            self.model.addItems([row[0] for row in cursor.fetchall()])

            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error populating dropdowns: {e}")

    def apply_filters(self):
        """Apply the selected filters and update the map pins."""
        filters = {
            "min_price": self.min_price.text(),
            "max_price": self.max_price.text(),
            "min_km": self.min_km.text(),
            "max_km": self.max_km.text(),
            "vehicle_type": self.vehicle_type.currentText(),
            "brand": self.brand.currentText(),
            "model": self.model.currentText(),
        }
        print(f"Applying filters: {filters}")  # Debug
        self.filter(filters)
        self.close()

    def filter(self, filters):
        """Filter the pins on the map based on the selected filters."""
        try:
            db = DB.Database()
            connection = db.connect()
            if connection is None:
                print("Failed to connect to the database.")
                return

            cursor = connection.cursor()

            # Build the query dynamically based on the filters
            query = """
                SELECT id, price_per_day, vehicle_type, brand, model, total_km, name_of_user, 
                street, number, city, country
                FROM vehicle_listing INNER JOIN User ON name_of_user = username 
                INNER JOIN address ON username_address = username
                WHERE vehicle_listing.status = 'listed'
            """
            params = []

            if filters["min_price"]:
                query += " AND price_per_day >= %s"
                params.append(filters["min_price"])
            if filters["max_price"]:
                query += " AND price_per_day <= %s"
                params.append(filters["max_price"])
            if filters["min_km"]:
                query += " AND total_km >= %s"
                params.append(filters["min_km"])
            if filters["max_km"]:
                query += " AND total_km <= %s"
                params.append(filters["max_km"])
            if filters["vehicle_type"] and filters["vehicle_type"] != "Any":
                query += " AND vehicle_type = %s"
                params.append(filters["vehicle_type"])
            if filters["brand"] and filters["brand"] != "Any":
                query += " AND brand = %s"
                params.append(filters["brand"])
            if filters["model"] and filters["model"] != "Any":
                query += " AND model = %s"
                params.append(filters["model"])

            cursor.execute(query, params)
            results = cursor.fetchall()

            # Debug: Print the results
            print(f"Filter results: {results}")

            # Clear existing pins and add new ones
            self.map_widget.clear_pins()
            for row in results:
                # Dynamically calculate latitude and longitude using a geocoding API
                address = f"{row[7]} {row[8]}, {row[9]}, {row[10]}"
                coords = self.get_coordinates_from_address_string(address)
                if coords:
                    pin = Pin(latitude=coords[0], longitude=coords[1], title=f"Listing ID: {row[0]}")
                    # Connect the click event to open_details_screen
                    pin.clicked.connect(lambda *args, l_id=row[0]: self.parent().open_details_screen(l_id))
                    self.map_widget.place(pin)

            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error applying filters: {e}")

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
