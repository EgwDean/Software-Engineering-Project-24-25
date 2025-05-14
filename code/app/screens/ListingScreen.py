from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from pathlib import Path
from screens.BookPage import BookPage

class ListingScreen(QWidget):
    def __init__(self, user, listing_data):
        super().__init__()
        self.user = user
        self.listing_data = listing_data
        self.setWindowTitle("Listing Details")
        self.setGeometry(200, 100, 700, 600)

        # Διεύθυνση του φακέλου με τις εικόνες
        self.assets_dir = Path(__file__).parent.parent.parent / 'assets' / 'images'

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Τίτλος
        title_label = QLabel("Listing Details")
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #007bff;")
        main_layout.addWidget(title_label)

        # Εικόνες: Προβολή στις πρώτες θέσεις χωρίς Scroll
        image_layout = QHBoxLayout()  # Οριζόντιο layout για τις εικόνες
        image_layout.setSpacing(10)

        # Φόρτωση εικόνων από το φάκελο
        for img_file in sorted(self.assets_dir.glob(f"img_{self.listing_data['id']}_*.jpg")):
            img_label = QLabel()
            pixmap = QPixmap(str(img_file)).scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            image_layout.addWidget(img_label)

        main_layout.addLayout(image_layout)

        # Κύριο πλέγμα πληροφοριών
        grid = QGridLayout()
        grid.setSpacing(15)

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

        row = 0
        for key, label_name in fields.items():
            value = self.listing_data.get(key, "N/A")

            # Ετικέτα τίτλου πεδίου
            label = QLabel(f"{label_name}:")
            label.setStyleSheet("font-weight: bold; font-size: 15px; color: #333;")
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # Ετικέτα τιμής πεδίου
            value_label = QLabel(f"{value}")
            value_label.setStyleSheet("font-size: 15px; color: #007bff;")
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            grid.addWidget(label, row, 0)
            grid.addWidget(value_label, row, 1)
            row += 1

        main_layout.addLayout(grid)

        # Οριζόντια γραμμή
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #ccc; margin: 10px 0;")
        main_layout.addWidget(line)

        # Κουμπί Book Now
        book_button = QPushButton("Rent Now")
        book_button.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                background-color: skyblue;
                color: white;
                border-radius: 8px;
                font-size: 16px;
            }
        """)
        book_button.clicked.connect(self.open_book_page)
        book_button.setFixedWidth(200)
        book_button.setCursor(Qt.PointingHandCursor)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(book_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def open_book_page(self):
        self.book_page = BookPage(self.user, self.listing_data)
        self.book_page.show()
        self.close()
        
