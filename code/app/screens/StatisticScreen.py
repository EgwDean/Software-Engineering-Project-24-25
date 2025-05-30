from services.FilterStatistics import FilterStatistics
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QLineEdit,
    QDialog, QCalendarWidget
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pathlib import Path
from services.Graph import Graph
from services.ExportStatistics import ExportStatistics
from screens.GraphScreen import GraphScreen

class StatisticScreen(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user
        self.setWindowTitle("Statistics")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(900, 520)

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

        # Main Content with Sidebar 
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

        graph_button = QPushButton("Show Graph")
        graph_button.setStyleSheet("""
            padding: 6px;
            font-size: 14px;
            background-color: #5cb85c;
            color: white;
            border: none;
            border-radius: 4px;
        """)
        graph_button.clicked.connect(self.showGraph)

        # Export Statistics
        export_button = QPushButton("Export Statistics")
        export_button.setStyleSheet(""" 
            padding: 6px;
            font-size: 14px;
            background-color: #f0ad4e;
            color: white;
            border: none;
            border-radius: 4px;
        """)
        export_button.clicked.connect(self.exportData)

        sidebar_layout.addWidget(self.brand_input)
        sidebar_layout.addWidget(self.model_input)
        sidebar_layout.addWidget(self.date_input)
        sidebar_layout.addWidget(self.vehicle_type_input)
        sidebar_layout.addWidget(self.status_input)
        sidebar_layout.addWidget(filter_button)
        sidebar_layout.addWidget(graph_button)
        sidebar_layout.addWidget(export_button)
        sidebar_layout.addStretch()

        sidebar_frame = QFrame()
        sidebar_frame.setLayout(sidebar_layout)
        sidebar_frame.setFixedWidth(180)
        sidebar_frame.setStyleSheet("background-color: #e0f7fa; padding: 10px;")
        content_layout.addWidget(sidebar_frame)

        # Table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Brand", "Model", "Vehicle Type", "Status", "Total Listings"])
        self.table_widget.setShowGrid(False)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.verticalHeader().setVisible(False)

        # Styling
        self.table_widget.setStyleSheet("""
            QTableWidget {
                font-size: 13px;
                border: none;
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 8px;
                border-bottom: 1px solid #dcdcdc;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #ecf0f1;
            }
            QScrollBar:vertical {
                border: none;
                background: #ecf0f1;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)


        content_layout.addWidget(self.table_widget)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        self.filter()

    def filter(self, brand_filter="", model_filter="", date_filter="", vehicle_type_filter="", status_filter=""):
        self.table_widget.setRowCount(0)
        try:
            results = FilterStatistics.fetchStatistics(brand_filter, model_filter, date_filter, vehicle_type_filter, status_filter)
            self.displayStatistics(results)
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

    def displayStatistics(self, results):
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

    def showGraph(self):
        try:
            results = FilterStatistics.fetchStatistics(
                self.brand_input.text().strip(),
                self.model_input.text().strip(),
                self.date_input.text().strip(),
                self.vehicle_type_input.text().strip(),
                self.status_input.text().strip()
            )

            # create the Graph object and generate graphs
            graph = Graph(results)
            graph_html_paths = graph.create_graphs()  # HTML files 

            # show the graphs in a new window
            self.graph_screen = GraphScreen(graph_html_paths)
            self.graph_screen.show()

        except Exception as e:
            error_label = QLabel(f"Error: {e}")
            self.layout().addWidget(error_label)


    def exportData(self):
        try:
            # get the filtered statistics
            results = FilterStatistics.fetchStatistics(
                self.brand_input.text().strip(),
                self.model_input.text().strip(),
                self.date_input.text().strip(),
                self.vehicle_type_input.text().strip(),
                self.status_input.text().strip()
            )

            # create a file dialog to select the save location
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)", options=options)

            # check if the user selected a file
            if file_path:
                # call the ExportStatistics class to save the results
                ExportStatistics.save_to_csv(results, file_path)

                self.show_success_message()

        except Exception as e:
            error_label = QLabel(f"Error: {e}")
            self.layout().addWidget(error_label)

    # show success message after exporting
    def show_success_message(self):
        success_msg = QMessageBox(self)
        success_msg.setIcon(QMessageBox.Information)
        success_msg.setWindowTitle("Export Successful")
        success_msg.setText("Statistics exported successfully!")
        success_msg.setStandardButtons(QMessageBox.Ok)
        success_msg.exec_()





