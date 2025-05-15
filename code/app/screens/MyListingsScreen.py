import services.Database as DB
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from functools import partial
from screens.ListEditingScreen import ListEditingScreen
from screens.ListingScreen import ListingScreen


class MyListingsScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"{self.user.username}'s Listings")
        self.setStyleSheet("background-color: #f0f0f0;")

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

        header_label = QLabel(f"Your Listings")
        header_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #007BFF;
            margin-left: 50px;
        """)
        top_layout.addWidget(header_label)

        # Adding the Refresh Button
        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        refresh_button.clicked.connect(self.refresh_screen)  # Connecting to the refresh method
        top_layout.addWidget(refresh_button)

        main_layout.addLayout(top_layout)

        # Listings layout
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
            no_listings_label = QLabel("No listings found!")
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
                view_more_button.clicked.connect(partial(self.open_listing_screen, listing))
                listing_layout.addWidget(view_more_button)

                # Edit Button
                edit_button = QPushButton("Edit")
                edit_button.setStyleSheet("""
                    padding: 10px 20px;
                    background-color: #ffc107;
                    color: white;
                    border-radius: 5px;
                    font-size: 14px;
                """)
                edit_button.clicked.connect(partial(self.open_edit_screen, listing))
                listing_layout.addWidget(edit_button)

                listing_frame.setLayout(listing_layout)
                self.listings_layout.addWidget(listing_frame)

    def open_listing_screen(self, listing_data):
        print("Opening ListingScreen")
        self.listing_screen = ListingScreen(self.user, listing_data)
        self.listing_screen.show()

    def open_edit_screen(self, listing_data):
        print("Opening ListEditingScreen")
        self.edit_screen = ListEditingScreen(self.user, listing_data)
        self.edit_screen.show()

    def fetch_listings_from_db(self, filters=None):
        try:
            db = DB.Database()
            db_connection = db.connect()
            if db_connection is None:
                print("Failed to connect to the database.")
                return []
            cursor = db_connection.cursor(dictionary=True)
            query = "SELECT * FROM vehicle_listing WHERE name_of_user = %s"
            params = [self.user.username]
            if filters and filters.get("brand"):
                query += " AND brand LIKE %s"
                params.append(f"%{filters['brand']}%")
            cursor.execute(query, tuple(params))
            listings = cursor.fetchall()
            cursor.close()
            db_connection.close()
            return listings
        except Exception as e:
            print(f"Error fetching listings: {e}")
            return []

    def back_to_map(self):
        self.close()

    def refresh_screen(self):
        # Refresh the listings by calling update_listings again
        self.update_listings()