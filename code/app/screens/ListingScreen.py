from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

class ListingScreen(QWidget):
    def __init__(self, user, listing_data):
        super().__init__()
        self.user = user
        self.listing_data = listing_data
        self.setWindowTitle("Listing Details")
        self.setGeometry(100, 100, 600, 600)

        layout = QGridLayout()

        fields = {
            "name_of_user": "Owner",
            "price_per_day": "Price per Day (€)",
            "vehicle_type": "Vehicle Type",
            "brand": "Brand",
            "model": "Model",
            "year": "Year",
            "total_km": "Total Kilometers",
            "fuel_type": "Fuel Type",
            "description": "Description",
            "from_date": "Available From",
            "to_date": "Available To"
        }

        row, col = 0, 0
        for key, label_name in fields.items():
            value = listing_data.get(key, "N/A")
            # Δημιουργία ετικέτας με τίτλο και τιμή
            label = QLabel(f"<b>{label_name}:</b> <span style='color: #007bff;'>{value}</span>")
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label.setStyleSheet("""
                font-size: 16px;
                margin-bottom: 10px;
                text-align: center;
                font-weight: bold;
            """)

            layout.addWidget(label, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        # Κουμπί Book Now
        book_button = QPushButton("Book Now")
        book_button.setStyleSheet("""
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            font-size: 16px;
        """)
        book_button.clicked.connect(self.open_book_page)
        layout.addWidget(book_button, row, 0, 1, 3)

        self.setLayout(layout)

    def open_book_page(self):
        self.book_page = BookPage(self.user, self.listing_data)
        self.book_page.show()
        self.close()
