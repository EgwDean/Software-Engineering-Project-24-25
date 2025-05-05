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
        self.setWindowTitle("Rental History")
        self.user = user
        self.setStyleSheet("background-color: #f9f9f9;")
        self.showMaximized()

        # Logo image path
        self.logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo_1.png'
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel(f"{self.user.username}'s Rental History")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        rentals = self._fetch_rentals()
        for rental in rentals:
            content_layout.addWidget(self._create_rental_box(rental))
        content_layout.addStretch()

    def _fetch_rentals(self):
        db = DB.Database()
        conn = db.connect()
        rentals = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT v.id, v.brand, v.model, v.year, r.from_date, r.number_of_days "
                "FROM rents r JOIN vehicle_listing v ON r.id_of_listing = v.id "
                "WHERE r.user_who_rents = %s",
                (self.user.username,)
            )
            rentals = cursor.fetchall()
            cursor.close()
            conn.close()
        return rentals

    def _has_reviewed(self, listing_id):
        db = DB.Database()
        conn = db.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM reviews WHERE name_reviewer = %s AND id_list_review = %s",
                (self.user.username, listing_id)
            )
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        finally:
            conn.close()

    def _has_reported(self, listing_id):
        db = DB.Database()
        conn = db.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM reports WHERE name_reporter = %s AND id_list_report = %s",
                (self.user.username, listing_id)
            )
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        finally:
            conn.close()

    def _create_rental_box(self, rental):
        box = QFrame()
        box.setStyleSheet(
            "QFrame { background-color: white; border: 1px solid #dcdcdc;"
            " border-radius: 10px; padding: 15px; }"
        )
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox = QHBoxLayout(box)

        img = QLabel()
        pix = QPixmap(str(self.logo_path)).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img.setPixmap(pix)
        img.setFixedSize(100, 100)
        hbox.addWidget(img)

        info = QVBoxLayout()
        info.addWidget(QLabel(f"Vehicle: {rental['brand']} {rental['model']} ({rental['year']})"))
        info.addWidget(QLabel(f"Rented on: {rental['from_date']}"))
        info.addWidget(QLabel(f"Duration: {rental['number_of_days']} days"))
        hbox.addLayout(info)

        btn_review = QPushButton("Review")
        btn_review.setFixedWidth(80)
        btn_review.clicked.connect(lambda _, r=rental: self._open_review(r))
        hbox.addWidget(btn_review, alignment=Qt.AlignRight)

        btn_report = QPushButton("Report")
        btn_report.setFixedWidth(80)
        btn_report.clicked.connect(lambda _, r=rental: self._open_report(r))
        hbox.addWidget(btn_report, alignment=Qt.AlignRight)

        return box

    def _open_review(self, rental):
        if self._has_reviewed(rental['id']):
            QMessageBox.information(self, "Already Reviewed", "You have already reviewed this rental.")
            return
        dialog = ReviewPage(self.user, rental['id'], self)
        dialog.exec_()

    def _open_report(self, rental):
        if self._has_reported(rental['id']):
            QMessageBox.information(self, "Already Reported", "You have already reported this rental.")
            return
        dialog = ReportPage(self.user, rental['id'], self)
        dialog.exec_()
