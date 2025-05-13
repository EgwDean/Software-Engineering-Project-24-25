from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
from screens.ListingsScreen import ListingsScreen

class MapScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Map Screen")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Make the window maximized
        self.showMaximized()

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

        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_bar.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: none;
            background-color: white;
            border-radius: 5px;
        """)
        top_menu_layout.addWidget(search_bar)

        # Filter icon
        filter_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-filter-30.png'
        if not filter_icon_path.exists():
            raise FileNotFoundError(f"Filter icon file not found at {filter_icon_path}")
        filter_label = QLabel()
        filter_pixmap = QPixmap(str(filter_icon_path))
        filter_label.setPixmap(filter_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        filter_label.setCursor(Qt.PointingHandCursor)
        filter_label.mousePressEvent = self.do_nothing
        top_menu_layout.addWidget(filter_label)

        # User icon as button
        user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {user_icon_path}")
        user_label = QLabel()
        user_pixmap = QPixmap(str(user_icon_path))
        user_label.setPixmap(user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        user_label.setCursor(Qt.PointingHandCursor)
        user_label.mousePressEvent = self.open_profile_screen  # Link to ProfileScreen
        top_menu_layout.addWidget(user_label)

        # Top menu frame
        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")
        main_layout.addWidget(top_menu_frame)

        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Navigation menu
        nav_menu = QVBoxLayout()
        nav_menu.setAlignment(Qt.AlignTop)

        for i in range(5):
            label = "VIEW ALL LISTINGS" if i == 0 else f"TODO {i + 1}"
            button = QPushButton(label)
            button.setStyleSheet("""
                padding: 8px 2px;                  
                font-size: 16px;                     
                background-color: #007BFF;          
                border: 2px solid #0056b3;          
                border-radius: 8px;                  
                color: white;                        
                text-align: center;                  
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); 
                font-weight: bold;                   
            """)
            # If it's the "VIEW ALL LISTINGS" button, connect to open_listings
            if i == 0:
                button.clicked.connect(self.open_listings)
            else:
                button.clicked.connect(self.do_nothing)
            nav_menu.addWidget(button)

        nav_menu.addStretch()

        nav_menu_frame = QFrame()
        nav_menu_frame.setLayout(nav_menu)
        nav_menu_frame.setFixedWidth(200)
        nav_menu_frame.setStyleSheet("background-color: skyblue;")
        content_layout.addWidget(nav_menu_frame)

        # OpenStreetMap View
        map_view = QWebEngineView()
        map_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Leaflet Map</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>html, body, #map { height: 100%; margin: 0; }</style>
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        </head>
        <body>
            <div id="map"></div>
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <script>
                var map = L.map('map').setView([51.505, -0.09], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
            </script>
        </body>
        </html>
        """
        map_view.setHtml(map_html)
        content_layout.addWidget(map_view)

        # Add to main layout
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def reload_page(self, event):
        self.close()
        self.__init__(self.user)
        self.show()

    def do_nothing(self, event):
        pass

    def open_listings(self, event=None):
        # Create and show the ListingsScreen window
        self.listings_window = ListingsScreen(self.user)
        self.listings_window.show()

    def open_profile_screen(self, event=None):
        # Αναβολή της εισαγωγής της ProfileScreen εδώ
        from screens.ProfileScreen import ProfileScreen  # Εισάγουμε την ProfileScreen μόνο όταν χρειάζεται
        self.profile_screen = ProfileScreen(self.user, self)  # Δημιουργούμε την ProfileScreen
        self.profile_screen.show()  # Εμφανίζουμε την ProfileScreen
        self.close()  # Κλείνουμε την MapScreen
