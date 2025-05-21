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
from screens.MenuScreen import MenuScreen  # Import the MenuScreen class
from screens.MapScreen import MapScreen  # Import the MapScreen class


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Initialize database connection
        self.db_connection = None

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
        frame.setFixedWidth(400)  # Set a fixed width for the frame
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Error message label (initialize before calling init_db_connection)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 12px; border: none;")  # No border
        self.error_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.error_label)

        # Call init_db_connection after initializing error_label
        self.init_db_connection()

        # Hardcoded logo path
        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'

        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found at {logo_path}")

        # Convert Path object to string
        logo_path_str = str(logo_path)

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
        self.username_input.textChanged.connect(self.check_fields)  # Connect to check_fields
        frame_layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.password_input.textChanged.connect(self.check_fields)  # Connect to check_fields
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
            QPushButton:pressed {
                background-color: #4682b4;  /* Darker blue for click effect */
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
                background-color: #87ceeb;  /* Lighter blue on hover */
            }
            QPushButton:pressed {
                background-color: #4682b4;  /* Darker blue for click effect */
            }
        """)
        self.login_button.setEnabled(False)  # Disable the login button by default
        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.open_signup_page)  # Connect to open_signup_page
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)

        frame_layout.addLayout(button_layout)
        frame.setLayout(frame_layout)

        # Add frame to main layout
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def check_fields(self):
        """Enable the login button only if both fields are filled."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if username and password:
            self.login_button.setEnabled(True)
            self.error_label.setText("")
        else:
            self.login_button.setEnabled(False)

    def init_db_connection(self):
        """Initialize the database connection."""
        try:
            db = DB.Database()
            self.db_connection = db.connect()

            if self.db_connection is None:
                self.error_label.setText("Failed to connect to the database.")
                print("Failed to connect to the database.")
        except Exception as e:
            self.error_label.setText("An error occurred while connecting to the database.")
            print(f"An error occurred while connecting to the database: {e}")

    def login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.error_label.setText("Both fields are required!")
            return None  # Return None if fields are empty

        try:
            if self.db_connection is None:
                self.error_label.setText("No database connection available.")
                return None

            # Call the login stored procedure
            cursor = self.db_connection.cursor()
            out_type = cursor.callproc('login', [username, password, None])

            # Retrieve the OUT parameter
            login_type = out_type[2]

            # Close the cursor
            cursor.close()

            # Handle the login type
            if login_type == 'user':
                print("Logged in as a user.")
                self.error_label.setText("")  # Clear any error messages
                self.map_screen = MapScreen(SU.StandardUser(username))  # Pass the user object to MapScreen
                self.map_screen.show()  # Show the MapScreen
                self.close()  # Close the LoginPage
                return SU.StandardUser(username)
            elif login_type == 'admin':
                print("Logged in as an admin.")
                self.error_label.setText("")  # Clear any error messages
                self.admin_window = MenuScreen(AD.Admin(username))
                self.admin_window.show()
                self.close()  # Close the LoginPage
                return AD.Admin(username)
            else:
                self.error_label.setText("Invalid credentials!")
                return None  

        except Exception as e:
            self.error_label.setText("An error occurred during login.")
            print(f"An error occurred: {e}")
            return None

    def open_signup_page(self):
        """Open the Sign Up page."""
        self.signup_page = SignUpPage()  # Create an instance of SignUpPage
        self.signup_page.show()  # Show the SignUpPage
        self.close()  # Close the LoginPage