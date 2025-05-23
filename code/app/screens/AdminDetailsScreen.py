import services.Database as DB
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QFrame, QPushButton, QSizePolicy, QSpacerItem, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from services.ReportHandler import ReportHandler  # import ReportHandler

class AdminDetailsScreen(QWidget):
    def __init__(self, admin_user, report_id):
        super().__init__()
        self.admin_user = admin_user
        self.report_id = report_id
        self.setWindowTitle("Report Details")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(620, 520)

        # instance ReportHandler
        self.report_handler = ReportHandler(self.report_id)
        self.refund_done = False  # Μεταβλητή ελέγχου για refund

        # layout for window
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Top menu
        top_menu_layout = QHBoxLayout()
        top_menu_layout.setAlignment(Qt.AlignLeft)

        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        logo_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        logo_label.setPixmap(pixmap.scaledToWidth(70, Qt.SmoothTransformation))
        logo_label.setCursor(Qt.PointingHandCursor)
        logo_label.mousePressEvent = self.back_to_management
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

        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #d9534f;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.clicked.connect(self.close_screen)
        top_menu_layout.addWidget(close_button)

        top_menu_frame = QFrame()
        top_menu_frame.setLayout(top_menu_layout)
        top_menu_frame.setStyleSheet("background-color: skyblue; padding: 10px;")

        # bar on layout
        main_vertical_layout.addWidget(top_menu_frame)

        # layout for table
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Left layout with report details
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(7) 
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Field", "Value"])
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setShowGrid(False)
        self.table_widget.setAlternatingRowColors(True)

        fields = ["Report by", "Owner of Vehicle", "Rented by", "Comment", "Date", "Listing ID", "Total Rent €"]
        for row_index, field in enumerate(fields):
            field_item = QTableWidgetItem(field)
            field_item.setFlags(Qt.ItemIsEnabled)
            self.table_widget.setItem(row_index, 0, field_item)

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
        """)

        left_layout.addWidget(self.table_widget)

        # Right panel 
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(20, 20, 20, 20)
        right_panel.setSpacing(20)
        right_panel.setAlignment(Qt.AlignTop)

        btn_style = """
            padding: 10px 20px;
            font-size: 14px;
            background-color: #5bc0de;
            color: white;
            border: none;
            border-radius: 5px;
        """

        self.refund_button = QPushButton("Refund")
        self.refund_button.setStyleSheet(btn_style)
        self.refund_button.setCursor(Qt.PointingHandCursor)
        self.refund_button.clicked.connect(self.handleRefund)

        self.suspend_button = QPushButton("Suspend Account")
        self.suspend_button.setStyleSheet(btn_style)
        self.suspend_button.setCursor(Qt.PointingHandCursor)
        self.suspend_button.clicked.connect(self.handleSuspend)

        self.ignore_button = QPushButton("Ignore")
        self.ignore_button.setStyleSheet(btn_style)
        self.ignore_button.setCursor(Qt.PointingHandCursor)
        self.ignore_button.clicked.connect(self.handleIgnore)

        self.complete_button = QPushButton("Complete")
        self.complete_button.setStyleSheet(btn_style)
        self.complete_button.setCursor(Qt.PointingHandCursor)
        self.complete_button.clicked.connect(self.handleComplete)

        right_panel.addWidget(self.refund_button)
        right_panel.addWidget(self.suspend_button)
        right_panel.addWidget(self.ignore_button)
        right_panel.addWidget(self.complete_button)
        right_panel.addStretch()

        # Spacer to push buttons to the top
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_panel)

        # Add a spacer to the right panel
        main_vertical_layout.addLayout(main_layout)


        self.setLayout(main_vertical_layout)

        self.fetchDetails()

    #get the report details from the database
    def fetchDetails(self):
        conn = DB.Database.connect()
        if not conn or not conn.is_connected():
            error_label = QLabel("Error: Cannot connect to the database")
            self.layout().addWidget(error_label)
            return

        # Fetch report details from the database
        cursor = conn.cursor()
        try:
            query = """
                SELECT name_reporter, name_of_user, user_who_rents, comment, date_of_report, id, price_per_day * number_of_days AS total
                FROM reports r 
                INNER JOIN vehicle_listing vl ON r.id_list_report = vl.id
                INNER JOIN rents re ON vl.id = re.id_of_listing
                WHERE id = %s
            """
            cursor.execute(query, (self.report_id,))
            result = cursor.fetchone()

            if result:
                for row_index, value in enumerate(result):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(Qt.ItemIsEnabled)
                    self.table_widget.setItem(row_index, 1, item)

                self.table_widget.resizeColumnsToContents()
            else:
                error_label = QLabel("No data found for this report.")
                self.layout().addWidget(error_label)

        except Exception as e:
            error_label = QLabel(f"Error: {e}")
            self.layout().addWidget(error_label)
        finally:
            cursor.close()
            conn.close()

    # handle the refund button, call the handler
    def handleRefund(self):
        if self.refund_done:
            QMessageBox.warning(self, "Refund Already Processed", "This report has already been refunded.")
            return

        self.report_handler.refund()
        self.refund_done = True
        self.refund_button.setEnabled(False)
        QMessageBox.information(self, "Refund Successful", "The refund was successfully processed.")

    # handle the suspend button, call the handler
    def handleSuspend(self):
        try:
            self.report_handler.suspendAccount()
            QMessageBox.information(self, "Account Suspended", "The related user account has been suspended.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to suspend account: {e}")

    # handle the ignore button, call the handler
    def handleIgnore(self):
        try:
            self.report_handler.ignore()
            QMessageBox.information(self, "Report Ignored", f"Report {self.report_id} marked as ignored.")
            self.close()
            from screens.ManagmentScreen import ManagmentScreen
            self.management_screen = ManagmentScreen(self.admin_user)
            self.management_screen.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to ignore report: {e}")

    # handle the complete button, call the handler
    def handleComplete(self):
        try:
            self.report_handler.completeReport()
            QMessageBox.information(self, "Report Completed", f"Report {self.report_id} marked as complete.")
            self.close()
            from screens.ManagmentScreen import ManagmentScreen
            self.management_screen = ManagmentScreen(self.admin_user)
            self.management_screen.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to complete report: {e}")

    # close the screen and go back to management
    def close_screen(self):
        from screens.ManagmentScreen import ManagmentScreen 
        self.management_screen = ManagmentScreen(self.admin_user)
        self.management_screen.show()
        self.close()

    
    def back_to_management(self, event):
        from screens.ManagmentScreen import ManagmentScreen
        self.management_screen = ManagmentScreen(self.admin_user)
        self.management_screen.show()
        self.close()

    def do_nothing(self, event):
        pass
