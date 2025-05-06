# screens/HistoryPage.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea,
    QHBoxLayout, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path
import services.Database as DB
from screens.ReviewPage import ReviewPage
from screens.ReportPage import ReportPage

class HistoryPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Rental History")
        self.setStyleSheet("background-color: #f5f5f5; border-radius: 10px;")
        self.showMaximized()

        # logo path
        self.logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel(f"{self.user.username}'s Rental History")
        title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #333;
            padding: 20px 0;
            text-align: center;
        """)
        main_layout.addWidget(title)

        # Scroll area for rental boxes
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        container = QWidget()
        self.content_layout = QVBoxLayout(container)
        self.scroll.setWidget(container)
        main_layout.addWidget(self.scroll)

        # Load rentals
        self._load_rentals()

    def _load_rentals(self):
        rentals = self._fetch_rentals()

        for r in rentals:
            self.content_layout.addWidget(self._create_rental_box(r))
        self.content_layout.addStretch()

    def _fetch_rentals(self):
        conn = DB.Database.connect()
        rentals = []
        if conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT v.id, v.brand, v.model, v.year, r.from_date, r.number_of_days
                  FROM rents r
                  JOIN vehicle_listing v ON r.id_of_listing = v.id
                 WHERE r.user_who_rents = %s
                """,
                (self.user.username,)
            )
            rentals = cur.fetchall()
            cur.close()
            conn.close()
        return rentals

    def _has_reviewed(self, listing_id):
        conn = DB.Database.connect()
        if not conn:
            return False
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT 1 FROM reviews WHERE name_reviewer=%s AND id_list_review=%s",
                (self.user.username, listing_id)
            )
            return cur.fetchone() is not None
        finally:
            conn.close()

    def _has_reported(self, listing_id):
        conn = DB.Database.connect()
        if not conn:
            return False
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT 1 FROM reports WHERE name_reporter=%s AND id_list_report=%s",
                (self.user.username, listing_id)
            )
            return cur.fetchone() is not None
        finally:
            conn.close()

    def _create_rental_box(self, rental):
        box = QFrame()
        box.setStyleSheet("""
            QFrame { 
                background-color: #ffffff; 
                border: 1px solid #e0e0e0; 
                border-radius: 12px; 
                padding: 20px;
                margin: 10px 0;
            }
            QFrame:hover {
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
        """)
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        hbox = QHBoxLayout(box)

        # Image (Logo)
        img = QLabel()
        pix = QPixmap(str(self.logo_path)).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img.setPixmap(pix)
        img.setFixedSize(100, 100)
        hbox.addWidget(img)

        # Info section
        info = QVBoxLayout()
        info.addWidget(QLabel(f"<b>{rental['brand']} {rental['model']} ({rental['year']})</b>"))
        info.addWidget(QLabel(f"<i>Rented on: {rental['from_date']}</i>"))
        info.addWidget(QLabel(f"<i>Duration: {rental['number_of_days']} days</i>"))
        hbox.addLayout(info)

        # Buttons for Review and Report
        btn_layout = QVBoxLayout()
        
        btn_review = QPushButton("Write a Review")
        btn_review.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_review.setFixedWidth(120)
        btn_review.clicked.connect(lambda _, r=rental: self._open_review(r))
        btn_layout.addWidget(btn_review)

        btn_report = QPushButton("Report Issue")
        btn_report.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        btn_report.setFixedWidth(120)
        btn_report.clicked.connect(lambda _, r=rental: self._open_report(r))
        btn_layout.addWidget(btn_report)

        hbox.addLayout(btn_layout)
        
        return box

    def _open_review(self, rental):
        if self._has_reviewed(rental['id']):
            QMessageBox.information(self, "Already Reviewed",
                                    "You have already reviewed this rental.")
            return
        dlg = ReviewPage(self.user, rental['id'], self)
        dlg.exec_()

    def _open_report(self, rental):
        if self._has_reported(rental['id']):
            QMessageBox.information(self, "Already Reported",
                                    "You have already reported this rental.")
            return
        dlg = ReportPage(self.user, rental['id'], self)
        dlg.exec_()
