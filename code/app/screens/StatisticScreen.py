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


class StatisticScreen(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user
        self.setWindowTitle("Statistics")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(800, 500)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top menu
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
        user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {user_icon_path}")
        user_label = QLabel()
        user_pixmap = QPixmap(str(user_icon_path))
        user_label.setPixmap(user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        user_label.setCursor(Qt.PointingHandCursor)
        user_label.mousePressEvent = self.do_nothing
        top_menu_layout.addWidget(user_label)

        # Welcome label
        username_label = QLabel(f"Welcome, {self.admin_user.username}!")
        username_label.setStyleSheet("font-size: 14px; color: white;")
        top_menu_layout.addWidget(username_label)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_menu_layout.addItem(spacer)

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

        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")
        main_layout.addWidget(top_menu_frame)

        # Content layout
        content_layout = QHBoxLayout()

        # Sidebar (Navigation)
        nav_menu = QVBoxLayout()
        nav_menu.setAlignment(Qt.AlignTop)

        back_button = QPushButton("Back to Menu")
        back_button.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            background-color: skyblue;
            color: white;
            border: none;
            text-align: left;
        """)
        back_button.clicked.connect(self.back_to_menu)

        back_button_frame = QFrame()
        back_button_frame.setStyleSheet("border: 2px solid #ccc; padding: 5px; border-radius: 5px;")
        back_button_layout = QVBoxLayout()
        back_button_layout.addWidget(back_button)
        back_button_frame.setLayout(back_button_layout)
        nav_menu.addWidget(back_button_frame)

        nav_menu.addStretch()
        nav_menu_frame = QFrame()
        nav_menu_frame.setLayout(nav_menu)
        nav_menu_frame.setFixedWidth(200)
        nav_menu_frame.setStyleSheet("background-color: skyblue;")
        content_layout.addWidget(nav_menu_frame)

        # Statistics table
        table_widget = QTableWidget()
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Brand", "Total Listings", "Completed Sales"])
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
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        table_widget.setAlternatingRowColors(True)

        # Fetch statistics from database
        conn = DB.Database.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT brand, COUNT(*), 
                    SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END)
                    FROM vehicle_listing
                    GROUP BY brand;
                """)
                results = cursor.fetchall()

                table_widget.setRowCount(len(results))
                for row_index, row_data in enumerate(results):
                    for col_index, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        item.setFlags(Qt.ItemIsEnabled)
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

        content_layout.addWidget(table_widget)
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

    def back_to_menu(self):
        from screens.MenuScreen import MenuScreen
        self.menu = MenuScreen(self.admin_user)
        self.menu.show()
        self.close()
