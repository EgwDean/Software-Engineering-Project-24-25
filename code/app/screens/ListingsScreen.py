from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt

class ListingsScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Listings Screen")
        self.setStyleSheet("background-color: #f0f0f0;")
        
        self.map_screen = None  # Αποθήκευση του αντικειμένου MapScreen

        # Make the window maximized
        self.showMaximized()

        # Main layout
        main_layout = QVBoxLayout()

        # Top layout (Header with Back button on the left)
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)  # Align everything to the left

        # Back to Map button at the top left
        back_button = QPushButton("Back to Map")
        back_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #f44336;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        back_button.clicked.connect(self.back_to_map)
        top_layout.addWidget(back_button)

        # Header with title in the center
        header_label = QLabel("All Listings")
        header_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #007BFF;
            margin-left: 50px;  # Add some space between back button and header text
        """)
        top_layout.addWidget(header_label)

        main_layout.addLayout(top_layout)

        # Content layout (To display listings)
        listings_layout = QVBoxLayout()

        # Example of listing items
        listings = [
            {"title": "Listing 1", "description": "Description of Listing 1", "price": "$500"},
            {"title": "Listing 2", "description": "Description of Listing 2", "price": "$750"},
            {"title": "Listing 3", "description": "Description of Listing 3", "price": "$300"},
            {"title": "Listing 4", "description": "Description of Listing 4", "price": "$950"},
            {"title": "Listing 5", "description": "Description of Listing 5", "price": "$1200"}
        ]

        for listing in listings:
            # Create a frame for each listing
            listing_frame = QFrame()
            listing_frame.setStyleSheet("""
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-bottom: 20px;
                padding: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            """)
            
            # Create a layout for the listing frame
            listing_layout = QVBoxLayout()
            
            # Title of the listing
            title_label = QLabel(listing["title"])
            title_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #333;
            """)
            listing_layout.addWidget(title_label)
            
            # Description of the listing
            description_label = QLabel(listing["description"])
            description_label.setStyleSheet("""
                font-size: 14px;
                color: #666;
                margin-bottom: 10px;
            """)
            listing_layout.addWidget(description_label)
            
            # Price of the listing
            price_label = QLabel(listing["price"])
            price_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #28a745;
            """)
            listing_layout.addWidget(price_label)
            
            # Button to view more details (optional)
            details_button = QPushButton("View Details")
            details_button.setStyleSheet("""
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            """)
            listing_layout.addWidget(details_button)
            
            # Set the layout of the listing frame
            listing_frame.setLayout(listing_layout)
            
            # Add the frame to the listings layout
            listings_layout.addWidget(listing_frame)

        # Add a scroll area for the listings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())  # Create a widget to hold the listings_layout
        container_widget = scroll_area.widget()
        container_widget.setLayout(listings_layout)
        main_layout.addWidget(scroll_area)

        # Set the main layout
        self.setLayout(main_layout)

    def back_to_map(self):
        if self.map_screen is None:  # Αν δεν υπάρχει ήδη ανοιχτό το MapScreen
            # Δημιουργία του MapScreen και αποθήκευση του στο map_screen
            from screens.MapScreen import MapScreen
            self.map_screen = MapScreen(self.user)
        
        # Εμφάνιση του MapScreen και κλείσιμο της τρέχουσας οθόνης
        self.map_screen.show()
        self.close()
