from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QFrame
from PyQt5.QtCore import Qt
from screens.MyListingsScreen import MyListingsScreen  # Εισάγουμε την MyListingsScreen

class ProfileScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Profile Screen")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Main layout
        main_layout = QVBoxLayout()

        # Add user info label
        user_label = QLabel(f"Welcome, {self.user.username}!")
        user_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(user_label)

        # Button to view listings
        self.view_listings_button = QPushButton("View My Listings")
        self.view_listings_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.view_listings_button.clicked.connect(self.open_my_listings_screen)  # Ανοίγουμε την νέα οθόνη
        main_layout.addWidget(self.view_listings_button)

        self.setLayout(main_layout)

    def open_my_listings_screen(self):
        """Open the MyListingsScreen for the logged-in user."""
        self.my_listings_screen = MyListingsScreen(self.user)  # Δημιουργούμε το νέο παράθυρο
        self.my_listings_screen.show()  # Εμφανίζουμε το νέο παράθυρο
        self.close()  # Κλείνουμε την ProfileScreen
