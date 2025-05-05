from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from pathlib import Path


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
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a seamless layout

        # Top menu layout
        top_menu_layout = QHBoxLayout()
        top_menu_layout.setAlignment(Qt.AlignLeft)

        # Logo
        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found at {logo_path}")
        logo_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        logo_label.setPixmap(pixmap.scaledToWidth(70, Qt.SmoothTransformation))  # Increased logo size
        logo_label.setCursor(Qt.PointingHandCursor)
        logo_label.mousePressEvent = self.reload_page  # Reload page when clicked
        top_menu_layout.addWidget(logo_label)

        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_bar.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: none;  /* Remove white outline */
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
        filter_label.mousePressEvent = self.do_nothing  # Clickable but does nothing
        top_menu_layout.addWidget(filter_label)

        # User icon
        user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {user_icon_path}")
        user_label = QLabel()
        user_pixmap = QPixmap(str(user_icon_path))
        user_label.setPixmap(user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        user_label.setCursor(Qt.PointingHandCursor)
        user_label.mousePressEvent = self.do_nothing  # Clickable but does nothing
        top_menu_layout.addWidget(user_label)

        # Add top menu to a frame
        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")
        main_layout.addWidget(top_menu_frame)

        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for seamless layout

        # Navigation menu on the left
        nav_menu = QVBoxLayout()
        nav_menu.setAlignment(Qt.AlignTop)

        # Add buttons to the navigation menu
        for i in range(5):  # Add 5 buttons as placeholders
            button = QPushButton(f"TODO {i + 1}")
            button.setStyleSheet("""
                padding: 10px;
                font-size: 14px;
                background-color: skyblue;
                border: none;  /* Remove button borders */
                color: white;
                text-align: left;
            """)
            button.clicked.connect(self.do_nothing)  # Buttons do nothing
            nav_menu.addWidget(button)

        # Add a spacer to push buttons to the top
        nav_menu.addStretch()

        # Add the navigation menu to a frame
        nav_menu_frame = QFrame()
        nav_menu_frame.setLayout(nav_menu)
        nav_menu_frame.setFixedWidth(200)  # Set a fixed width for the navigation menu
        nav_menu_frame.setStyleSheet("background-color: skyblue;")
        content_layout.addWidget(nav_menu_frame)

        # Placeholder for the main content area
        main_content = QLabel("Main Content Area")
        main_content.setAlignment(Qt.AlignCenter)
        main_content.setStyleSheet("font-size: 18px; color: gray;")
        content_layout.addWidget(main_content)

        # Add content layout to the main layout
        main_layout.addLayout(content_layout)

        # Set the main layout
        self.setLayout(main_layout)

    def reload_page(self, event):
        """Reload the page when the logo is clicked."""
        self.close()
        self.__init__(self.user)
        self.show()

    def do_nothing(self, event):
        """Placeholder for clickable elements that do nothing."""
        pass