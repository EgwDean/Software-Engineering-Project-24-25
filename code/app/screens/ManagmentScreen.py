import services.Database as DB
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QFrame, QPushButton, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ManagmentScreen(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user
        self.setWindowTitle("Report Handling")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(900, 520)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === Top menu (ίδιο με MenuScreen) ===
        top_menu_layout = QHBoxLayout()
        top_menu_layout.setAlignment(Qt.AlignLeft)

        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        logo_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        logo_label.setPixmap(pixmap.scaledToWidth(70, Qt.SmoothTransformation))
        logo_label.setCursor(Qt.PointingHandCursor)
        logo_label.mousePressEvent = self.back_to_menu
        top_menu_layout.addWidget(logo_label)

        admin_user_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'icons8-user-30.png'
        admin_user_label = QLabel()
        admin_user_pixmap = QPixmap(str(admin_user_icon_path))
        admin_user_label.setPixmap(admin_user_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        admin_user_label.setCursor(Qt.PointingHandCursor)
        admin_user_label.mousePressEvent = self.do_nothing
        top_menu_layout.addWidget(admin_user_label)

        username_label = QLabel(f"Welcome, {self.admin_user.username}!")
        username_label.setStyleSheet("font-size: 14px; margin-left: 0px; color: white;")
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

        # === Table ===
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Reporter", "Comment", "Date of Report", "Listing ID", "Status"])
        self.table_widget.setShowGrid(False)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.verticalHeader().setVisible(False)

        # Custom styling με padding αριστερά και φαρδιά κελιά
        self.table_widget.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: none;
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
                padding-left: 20px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
                border-bottom: 1px solid #dcdcdc;
            }
            QTableWidget::item {
                padding: 12px;
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
                width: 10px;
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

        main_layout.addWidget(self.table_widget)
        self.setLayout(main_layout)

        self.load_reports()

    def load_reports(self):
        self.table_widget.setRowCount(0)
        conn = DB.Database.connect()
        if not conn or not conn.is_connected():
            error_label = QLabel("Error: Cannot connect to the database")
            self.layout().addWidget(error_label)
            return

        cursor = conn.cursor()
        try:
            query = """
                SELECT name_reporter, comment, date_of_report, id_list_report, status
                FROM reports
            """
            cursor.execute(query)
            results = cursor.fetchall()

            self.table_widget.setRowCount(len(results))
            for row_index, row_data in enumerate(results):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setFlags(Qt.ItemIsEnabled)
                    self.table_widget.setItem(row_index, col_index, item)

            # Αυτόματη προσαρμογή του πλάτους των στηλών σύμφωνα με το περιεχόμενο
            self.table_widget.resizeColumnsToContents()

        except Exception as e:
            error_label = QLabel(f"Error: {e}")
            self.layout().addWidget(error_label)
        finally:
            cursor.close()
            conn.close()

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
