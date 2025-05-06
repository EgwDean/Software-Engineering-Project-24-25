from services.FilterStatistics import FilterStatistics
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QLineEdit,
    QDialog, QCalendarWidget
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
from pathlib import Path

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

        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found at {logo_path}")
        logo_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        logo_label.setPixmap(pixmap.scaledToWidth(70, Qt.SmoothTransformation))
        logo_label.setCursor(Qt.PointingHandCursor)
        logo_label.mousePressEvent = self.back_to_menu
        top_menu_layout.addWidget(logo_label)

        user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        if not user_icon_path.exists():
            raise FileNotFoundError(f"User icon file not found at {user_icon_path}")
        user_label = QLabel()
        user_pixmap = QPixmap(str(user_icon_path))
        user_label.setPixmap(user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        user_label.setCursor(Qt.PointingHandCursor)
        user_label.mousePressEvent = self.do_nothing
        top_menu_layout.addWidget(user_label)

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

        # --- Main Content with Sidebar ---
        content_layout = QHBoxLayout()

        # Sidebar with filters
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setSpacing(10)

        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Brand")
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Model")

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Date of Listing (YYYY-MM-DD)")
        self.date_input.setReadOnly(True)
        self.date_input.setStyleSheet("background-color: white;")
        self.date_input.mousePressEvent = self.show_calendar

        self.vehicle_type_input = QLineEdit()
        self.vehicle_type_input.setPlaceholderText("Vehicle Type")

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Status")

        filter_button = QPushButton("Filter")
        filter_button.setStyleSheet(""" 
            padding: 6px;
            font-size: 14px;
            background-color: #5bc0de;
            color: white;
            border: none;
            border-radius: 4px;
        """)
        filter_button.clicked.connect(self.apply_filters)

        sidebar_layout.addWidget(self.brand_input)
        sidebar_layout.addWidget(self.model_input)
        sidebar_layout.addWidget(self.date_input)
        sidebar_layout.addWidget(self.vehicle_type_input)
        sidebar_layout.addWidget(self.status_input)
        sidebar_layout.addWidget(filter_button)
        sidebar_layout.addStretch()

        sidebar_frame = QFrame()
        sidebar_frame.setLayout(sidebar_layout)
        sidebar_frame.setFixedWidth(180)
        sidebar_frame.setStyleSheet("background-color: #e0f7fa; padding: 10px;")
        content_layout.addWidget(sidebar_frame)

        # Table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)  # 5 columns (brand, model, vehicle_type, status, count)
        self.table_widget.setHorizontalHeaderLabels(["Brand", "Model", "Vehicle Type", "Status", "Total Listings"])
        self.table_widget.setStyleSheet(""" 
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
        self.table_widget.setShowGrid(True)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setAlternatingRowColors(True)

        content_layout.addWidget(self.table_widget)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        self.filter()

    def filter(self, brand_filter="", model_filter="", date_filter="", vehicle_type_filter="", status_filter=""):
        self.table_widget.setRowCount(0)
        try:
            results = FilterStatistics.fetch_statistics(brand_filter, model_filter, date_filter, vehicle_type_filter, status_filter)
            self.display_statistics(results)
        except Exception as e:
            error_label = QLabel(f"Error: {e}")
            self.layout().addWidget(error_label)

    def apply_filters(self):
        brand = self.brand_input.text().strip()
        model = self.model_input.text().strip()
        date = self.date_input.text().strip()
        vehicle_type = self.vehicle_type_input.text().strip()
        status = self.status_input.text().strip()
        self.filter(brand_filter=brand, model_filter=model, date_filter=date, vehicle_type_filter=vehicle_type, status_filter=status)

    def display_statistics(self, results):
        # Populate the table with the results
        self.table_widget.setRowCount(len(results))
        for row_index, row_data in enumerate(results):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(Qt.ItemIsEnabled)
                self.table_widget.setItem(row_index, col_index, item)

    def show_calendar(self, event):
        calendar_dialog = QDialog(self)
        calendar_dialog.setWindowTitle("Select Date")
        calendar_dialog.setModal(True)
        layout = QVBoxLayout()
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setMaximumDate(QDate.currentDate())
        layout.addWidget(calendar)

        select_btn = QPushButton("Select Date")
        select_btn.clicked.connect(lambda: self.set_date_from_calendar(calendar.selectedDate(), calendar_dialog))
        layout.addWidget(select_btn)

        calendar_dialog.setLayout(layout)
        calendar_dialog.exec_()

    def set_date_from_calendar(self, selected_date, dialog):
        self.date_input.setText(selected_date.toString("yyyy-MM-dd"))
        dialog.accept()

    def logout(self):
        from screens.LoginPage import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()

    def back_to_menu(self, event):
        from screens.MenuScreen import MenuScreen
        self.menu = MenuScreen(self.admin_user)
        self.menu.show()
        self.close()

    def do_nothing(self, event):
        pass
