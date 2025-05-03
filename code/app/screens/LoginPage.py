from services.Database import Database
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Hardcoded logo path
        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'

        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found at {logo_path}")

        # Convert Path object to string
        logo_path_str = str(logo_path)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Frame for content
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #dcdcdc;
            }
        """)
        frame.setFixedWidth(int(self.width() * 0.5)) 
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Add shadow effect to the frame
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(Qt.black)
        frame.setGraphicsEffect(shadow)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(logo_path_str)
        logo_label.setPixmap(pixmap.scaledToWidth(200, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter) 
        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        frame_layout.addWidget(logo_label, alignment=Qt.AlignHCenter)

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 8px; font-size: 14px;")
        frame_layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; font-size: 14px;")
        frame_layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: skyblue;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #87ceeb;
            }
        """)
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: skyblue;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #87ceeb;
            }
        """)
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)

        frame_layout.addLayout(button_layout)
        frame.setLayout(frame_layout)

        self.login_button.clicked.connect(self.login)

        # Add frame to main layout
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def login(self): # TODO
        username = self.username_input.text()
        password = self.password_input.text()

        db = Database()
        db.connect()