import re  # Import the regular expressions module
import services.Database as DB
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from pathlib import Path


class SignUpPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up Page")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Initialize database connection
        self.db_connection = None
        self.init_db_connection()

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
        frame.setFixedWidth(400)
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

        # Phone field
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone (10-digit number)")
        self.phone_input.setStyleSheet("padding: 8px; font-size: 14px;")
        frame_layout.addWidget(self.phone_input)

        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("padding: 8px; font-size: 14px;")
        frame_layout.addWidget(self.email_input)

        # Country field
        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("Country")
        self.country_input.setStyleSheet("padding: 8px; font-size: 14px;")
        frame_layout.addWidget(self.country_input)

        # City field
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("City")
        self.city_input.setStyleSheet("padding: 8px; font-size: 14px;")
        frame_layout.addWidget(self.city_input)

        # Street field
        self.street_input = QLineEdit()
        self.street_input.setPlaceholderText("Street")
        self.street_input.setStyleSheet("padding: 8px; font-size: 14px;")
        frame_layout.addWidget(self.street_input)

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 12px; border: none;")
        self.error_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.error_label)

        # Buttons
        button_layout = QHBoxLayout()
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: skyblue;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: #4682b4;  /* Darker blue for click effect */
            }
        """)
        self.signup_button.clicked.connect(self.sign_up)
        button_layout.addWidget(self.signup_button)

        frame_layout.addLayout(button_layout)
        frame.setLayout(frame_layout)

        # Add frame to main layout
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def init_db_connection(self):
        """Initialize the database connection."""
        try:
            db = DB.Database()
            self.db_connection = db.connect()

            if self.db_connection is None:
                print("Failed to connect to the database.")
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")

    def validate_inputs(self):
        """Validate phone and email inputs."""
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        # Validate phone number (10-digit integer)
        if not re.fullmatch(r"\d{10}", phone):
            self.error_label.setText("Phone must be a 10-digit number.")
            return False

        # Validate email format
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            self.error_label.setText("Invalid email format.")
            return False

        return True

    def sign_up(self):
        """Handle sign-up logic."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        country = self.country_input.text().strip()
        city = self.city_input.text().strip()
        street = self.street_input.text().strip()

        if not all([username, password, phone, email, country, city, street]):
            self.error_label.setText("All fields are required!")
            return

        if not self.validate_inputs():
            return

        try:
            if self.db_connection is None:
                print("No database connection available.")
                return

            # Insert user into the user table
            cursor = self.db_connection.cursor()
            user_query = """
                INSERT INTO user (username, password, phone, email, balance, bank_id, message)
                VALUES (%s, %s, %s, %s, 0, NULL, NULL)
            """
            cursor.execute(user_query, (username, password, phone, email))

            # Insert address into the address table
            address_query = """
                INSERT INTO address (username_address, country, city, street)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(address_query, (username, country, city, street))

            # Commit the transaction
            self.db_connection.commit()

            # Close the cursor
            cursor.close()

            # Success message
            self.error_label.setStyleSheet("color: green; font-size: 12px; border: none;")
            self.error_label.setText("Account created successfully!")

        except Exception as e:
            print(f"An error occurred during sign-up: {e}")
            self.error_label.setText("Failed to create account. Try again.")
