import services.Database as DB
import entities.StandardUser as SU
import entities.Admin as AD
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from screens.StatisticScreen import StatisticScreen  # Import the MenuScreen class

class MenuScreen(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user
        self.setWindowTitle("Admin Menu")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(800, 500)  # Set a fixed size for the window

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

        # User icon
        admin_user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not admin_user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {admin_user_icon_path}")
        admin_user_label = QLabel()
        admin_user_pixmap = QPixmap(str(admin_user_icon_path))
        admin_user_label.setPixmap(admin_user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        admin_user_label.setCursor(Qt.PointingHandCursor)
        admin_user_label.mousePressEvent = self.do_nothing
        top_menu_layout.addWidget(admin_user_label)

        # Username label
        username_label = QLabel(f"Welcome, {self.admin_user.username}!")
        username_label.setStyleSheet("font-size: 14px; margin-left: 0px; color: white;")
        top_menu_layout.addWidget(username_label)

        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_menu_layout.addItem(spacer)

        # Logout button
        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #d9534f;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        logout_button.setCursor(Qt.PointingHandCursor)
        logout_button.clicked.connect(self.logout)
        top_menu_layout.addWidget(logout_button)

        # Top menu frame
        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")
        main_layout.addWidget(top_menu_frame)

        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Navigation menu
        nav_menu = QVBoxLayout()
        nav_menu.setAlignment(Qt.AlignTop)

        # Adding "Report Handling" button with frame
        report_button = QPushButton("Report Handling")
        report_button.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: white;
            text-align: left;
        """)
        report_button.clicked.connect(self.report_handling)

        # Frame for Report Handling button
        report_button_frame = QFrame()
        report_button_frame.setStyleSheet("border: 2px solid #ccc; padding: 5px; border-radius: 5px;")
        report_button_layout = QVBoxLayout()
        report_button_layout.addWidget(report_button)
        report_button_frame.setLayout(report_button_layout)
        nav_menu.addWidget(report_button_frame)

        # Adding "View Statistics" button with frame
        statistics_button = QPushButton("View Statistics")
        statistics_button.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            border: none;
            color: white;
            text-align: left;
        """)
        statistics_button.clicked.connect(self.displayStatisticScreen)

        # Frame for View Statistics button
        statistics_button_frame = QFrame()
        statistics_button_frame.setStyleSheet("border: 2px solid #ccc; padding: 5px; border-radius: 5px;")
        statistics_button_layout = QVBoxLayout()
        statistics_button_layout.addWidget(statistics_button)
        statistics_button_frame.setLayout(statistics_button_layout)
        nav_menu.addWidget(statistics_button_frame)

        nav_menu.addStretch()

        nav_menu_frame = QFrame()
        nav_menu_frame.setLayout(nav_menu)
        nav_menu_frame.setFixedWidth(200)
        nav_menu_frame.setStyleSheet("background-color: skyblue;")
        content_layout.addWidget(nav_menu_frame)

        # Create the table widget for vehicle listings
        table_widget = QTableWidget()
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(["Listing id", "User", "Brand", "Model"])
        table_widget.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                gridline-color: #ccc;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: lightgray;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        table_widget.setShowGrid(True)
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing
        table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        table_widget.setAlternatingRowColors(True)

        # Title for the table section (Latest) above the table
        latest_label = QLabel("Latest")
        latest_label.setAlignment(Qt.AlignCenter)
        latest_label.setStyleSheet("""
            font-size: 18px;
            font-style: italic;
            color: #333;
            font-family: 'Arial', sans-serif;
            margin-bottom: 10px;
        """)
        
        # Add the "Latest" label above the table
        content_layout.addWidget(latest_label)

        # Connect to the database and fetch the data
        conn = DB.Database.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id, name_of_user, brand, model FROM vehicle_listing WHERE status = 'completed' LIMIT 5;")
                results = cursor.fetchall()

                table_widget.setRowCount(len(results))
                for row_index, row_data in enumerate(results):
                    for col_index, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        item.setFlags(Qt.ItemIsEnabled)  # Non-editable
                        table_widget.setItem(row_index, col_index, item)

            except Exception as e:
                error_label = QLabel(f"Error: {e}")
                content_layout.addWidget(error_label)
            finally:
                cursor.close()
                conn.close()
        else:
            error_label = QLabel("Could not connect to database.")
            content_layout.addWidget(error_label)

        # Add the table widget below the "Latest" title
        content_layout.addWidget(table_widget)

        # Set the layout of the main window
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def reload_page(self, event):
        self.close()
        self.__init__(self.admin_user)
        self.show()

    def logout(self):
        from screens.LoginPage import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()

    def do_nothing(self, event):
        pass

    # Method for handling the "Report Handling" button
    def report_handling(self):
        print("Report Handling is clicked!")
        # Add your logic for Report Handling here

    # Method for handling the "View Statistics" button
    def displayStatisticScreen(self):
        print("View Statistics is clicked!")
        self.admin_window = StatisticScreen(AD.Admin(self.admin_user.username))  # Create an instance of StatisticScreen
        self.admin_window.show()  # Show the StatisticScreen window
        self.close()  # Close the current MenuScreen window
