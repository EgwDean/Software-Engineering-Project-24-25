import services.Database as DB
import entities.StandardUser as SU
import entities.Admin as AD
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  # Add this line
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

class MenuScreen(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user
        self.setWindowTitle("Admin Menu")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Hardcoded logo path
        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'

        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found at {logo_path}")

        # Convert Path object to string
        logo_path_str = str(logo_path)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Frame for content
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #dcdcdc;
            }
        """)
        # Allow the frame to expand and fill the available space
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Add shadow effect to the frame
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(Qt.black)
        frame.setGraphicsEffect(shadow)

        # Top layout (for logo, logout, and welcome message)
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignTop)

        # Logo (on the left)
        logo_label = QLabel()
        pixmap = QPixmap(logo_path_str)
        
        # Scale the image to a fixed size
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)  # Set the scaled pixmap to the label
        logo_label.setAlignment(Qt.AlignLeft)

        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        top_layout.addWidget(logo_label)

        # Add space between logo and other elements
        top_layout.addStretch()

        # Logout button and welcome message (on the right)
        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: darkred;
            }
            QPushButton:hover {
                background-color: darkorange;  /* Change to orange on hover */
            }
        """)
        logout_button.clicked.connect(self.logout)

        welcome_label = QLabel(f"Welcome, Admin: {self.admin_user.username}")
        welcome_label.setStyleSheet("font-size: 14px; color: #333; padding-right: 6px;")

        # Add the logout button and welcome label to top_layout
        top_layout.addWidget(welcome_label)
        top_layout.addWidget(logout_button)

        # Add top_layout to the frame layout
        frame_layout.addLayout(top_layout)

        # Add space between the top section and the buttons
        frame_layout.addStretch()  # This pushes the buttons further down

        # Center layout (for the buttons)
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)  # Center the buttons vertically

        # Create buttons for future functionality (1 and 2 as placeholders)
        button_1 = QPushButton("1")
        button_2 = QPushButton("2")

        # Button styling with hover effect
        button_style = """
            QPushButton {
                background-color: skyblue;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 5px;
                margin-bottom: 10px;  /* Add space between buttons */
            }
            QPushButton:pressed {
                background-color: #4682b4;
            }
            QPushButton:hover {
                background-color: #5a9bd5;  /* Lighter blue on hover */
            }
        """

        button_1.setStyleSheet(button_style)
        button_2.setStyleSheet(button_style)

        # Add buttons to the layout
        button_layout.addWidget(button_1)
        button_layout.addWidget(button_2)

        # Add button layout to the frame layout
        frame_layout.addLayout(button_layout)

        # Add stretch to push the buttons to the center
        frame_layout.addStretch()  # Ensure buttons stay centered

        # Set the layout for the frame
        frame.setLayout(frame_layout)

        # Add the frame to the main layout
        main_layout.addWidget(frame)

        # Set the layout for the widget
        self.setLayout(main_layout)

        # Set the minimum size of the window
        self.setMinimumSize(500, 400)

    def logout(self):
        """Handles logout button click to return to LoginPage."""
        from screens.LoginPage import LoginPage  # Import only when needed to avoid circular import
        self.login_page = LoginPage()  # Create an instance of LoginPage
        self.login_page.show()  # Show the LoginPage
        self.close()  # Close the current MenuScreen

