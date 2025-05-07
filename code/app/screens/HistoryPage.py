from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea,
    QHBoxLayout, QFrame, QSizePolicy, QMessageBox, QComboBox, QDateEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from pathlib import Path
import services.Database as DB
from screens.ReviewPage import ReviewPage
from screens.ReportPage import ReportPage

class HistoryPage(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Rental History")
        self.setStyleSheet("background-color: #f5f5f5;")
        self.showMaximized()

        self.assets_dir = Path(__file__).parent.parent.parent / 'assets'
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Back button
        back_btn = QPushButton("←")
        back_btn.setFixedSize(60, 60)
        back_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: #f44336; font-size: 36px; }"
            "QPushButton:hover { color: #d32f2f; }"
        )
        back_btn.clicked.connect(self.back_requested.emit)
        main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Title
        title = QLabel(f"{self.user.username}'s Rental History")
        title.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #333; padding: 20px 0;"
        )
        main_layout.addWidget(title)

        # Controls: Sort + Date Range
        controls = QHBoxLayout()
        controls.setSpacing(20)

        # Sort dropdown
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Sort by Date ↑", "Sort by Date ↓",
            "Sort by Duration ↑", "Sort by Duration ↓"
        ])
        self.sort_combo.setStyleSheet("font-size: 14px; padding: 4px;")
        controls.addWidget(self.sort_combo)

        # Date range
        controls.addWidget(QLabel("From:"))
        self.date_from = QDateEdit(calendarPopup=True)
        self.date_from.setDate(QDate.currentDate().addYears(-3))
        controls.addWidget(self.date_from)

        controls.addWidget(QLabel("To:"))
        self.date_to = QDateEdit(calendarPopup=True)
        self.date_to.setDate(QDate.currentDate())
        controls.addWidget(self.date_to)

        # Apply
        apply_btn = QPushButton("Apply")
        apply_btn.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; padding: 6px 12px;"
            " border-radius: 4px; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        apply_btn.clicked.connect(self._apply_filter_and_sort)
        controls.addWidget(apply_btn)

        controls_container = QWidget()
        controls_container.setLayout(controls)
        controls_container.setStyleSheet("margin: 10px 0;")
        main_layout.addWidget(controls_container)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        container = QWidget()
        self.content_layout = QVBoxLayout(container)
        self.scroll.setWidget(container)
        main_layout.addWidget(self.scroll)

        # Initial load
        self._apply_filter_and_sort()

    def _apply_filter_and_sort(self):
        # clear
        for i in reversed(range(self.content_layout.count())):
            w = self.content_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        # fetch with date range
        from_date = self.date_from.date().toString("yyyy-MM-dd")
        to_date   = self.date_to.date().toString("yyyy-MM-dd")
        rentals = self._fetch_rentals(from_date, to_date)

        # sort in Python
        key = self.sort_combo.currentText()
        if "Date ↑" in key:
            rentals.sort(key=lambda x: x['from_date'])
        elif "Date ↓" in key:
            rentals.sort(key=lambda x: x['from_date'], reverse=True)
        elif "Duration ↑" in key:
            rentals.sort(key=lambda x: x['number_of_days'])
        elif "Duration ↓" in key:
            rentals.sort(key=lambda x: x['number_of_days'], reverse=True)

        # display
        for r in rentals:
            self.content_layout.addWidget(self._create_rental_box(r))
        self.content_layout.addStretch()

    def _fetch_rentals(self, from_date, to_date):
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
                   AND r.from_date BETWEEN %s AND %s
                """,
                (self.user.username, from_date, to_date)
            )
            rentals = cur.fetchall()
            cur.close()
            conn.close()
        return rentals

    def _has_reviewed(self, listing_id):
        conn = DB.Database.connect()
        if not conn: return False
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
        if not conn: return False
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
        box.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #e0e0e0;"
            " border-radius: 12px; padding: 20px; margin: 10px 0; }"
        )
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox = QHBoxLayout(box)

        # image
        img = QLabel()
        img.setFixedSize(100, 100)
        img.setScaledContents(True)
        img_file = self.assets_dir / f"img_{rental['id']}_1.jpg"
        pix = QPixmap(str(img_file)) if img_file.exists() else QPixmap(str(self.assets_dir / 'logo_1.png'))
        img.setPixmap(pix)
        hbox.addWidget(img)

        # info
        info = QVBoxLayout()
        info.addWidget(QLabel(f"<b>{rental['brand']} {rental['model']} ({rental['year']})</b>"))
        info.addWidget(QLabel(f"<i>Rented on: {rental['from_date']}</i>"))
        info.addWidget(QLabel(f"<i>Duration: {rental['number_of_days']} days</i>"))
        hbox.addLayout(info)

        # actions
        btn_layout = QVBoxLayout()
        btn_review = QPushButton("Write a Review")
        btn_review.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; padding: 8px 16px;"
            " border-radius: 5px; font-weight: bold; border: none; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        btn_review.clicked.connect(lambda _,r=rental: self._open_review(r))
        btn_layout.addWidget(btn_review)

        btn_report = QPushButton("Report Issue")
        btn_report.setStyleSheet(
            "QPushButton { background-color: #f44336; color: white; padding: 8px 16px;"
            " border-radius: 5px; font-weight: bold; border: none; }"
            "QPushButton:hover { background-color: #e53935; }"
        )
        btn_report.clicked.connect(lambda _,r=rental: self._open_report(r))
        btn_layout.addWidget(btn_report)

        hbox.addLayout(btn_layout)
        return box

    def _open_review(self, rental):
        if self._has_reviewed(rental['id']):
            QMessageBox.information(self, "Already Reviewed", "You have already reviewed this rental.")
            return
        dlg = ReviewPage(self.user, rental['id'], self)
        dlg.exec_()

    def _open_report(self, rental):
        if self._has_reported(rental['id']):
            QMessageBox.information(self, "Already Reported", "You have already reported this rental.")
            return
        dlg = ReportPage(self.user, rental['id'], self)
        dlg.exec_()
