import services.Database as DB
import entities.StandardUser as SU
import entities.Admin as AD
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from screens.SignUpPage import SignUpPage  # Import the SignUpPage class


class MenuScreen(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user
        self.setWindowTitle("Admin Menu")

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Welcome label with admin username
        welcome_label = QLabel(f"Welcome, Admin: {self.admin_user.username}")
        welcome_label.setStyleSheet("font-size: 20px; color: #333;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Set the layout
        self.setLayout(layout)
        self.setMinimumSize(400, 200)