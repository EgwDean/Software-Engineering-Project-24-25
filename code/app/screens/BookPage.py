from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea,
    QDateEdit, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QPixmap, QTextCharFormat, QColor
from pathlib import Path
from datetime import datetime, timedelta
import services.Database as DB

class BookPage(QWidget):
    back_requested = pyqtSignal()
    booking_confirmed = pyqtSignal()

    def __init__(self, user, listing):
        super().__init__()
        self.user = user
        self.listing = listing
        self.unavailable = []  # list of (start_date, end_date)
        self.setWindowTitle("Book Listing")
        self.setStyleSheet("background-color: #f5f5f5;")
        self.showMaximized()
        self.assets_dir = Path(__file__).parent.parent.parent / 'assets' / 'images'
        self._load_unavailable_dates()
        self._setup_ui()
        self._customize_calendars()

    def _load_unavailable_dates(self):
        db = DB.Database()
        conn = db.connect()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            "SELECT from_date, number_of_days FROM rents WHERE id_of_listing = %s",
            (self.listing['id'],)
        )
        for start_str, days in cur.fetchall():
            start = datetime.strptime(str(start_str), '%Y-%m-%d').date()
            end = start + timedelta(days=days)
            self.unavailable.append((start, end))
        cur.close()
        conn.close()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Top bar with back and balance
        top_bar = QHBoxLayout()
        back_btn = QPushButton("←")
        back_btn.setFixedSize(40, 40)
        back_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: skyblue; font-size: 36px; }"
            "QPushButton:hover { color: deepskyblue; }"
        )
        back_btn.clicked.connect(self.close)
        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        balance_lbl = QLabel(f"Balance: €{self.user.balance:.2f}")
        balance_lbl.setStyleSheet("font-size: 18px; padding: 10px; color: #333;")
        top_bar.addWidget(balance_lbl)
        layout.addLayout(top_bar)

        # Image gallery
        gallery = QScrollArea()
        gallery.setWidgetResizable(True)
        container = QWidget()
        g_layout = QHBoxLayout(container)
        for img_file in sorted(self.assets_dir.glob(f"img_{self.listing['id']}_*.jpg")):
            lbl = QLabel()
            pix = QPixmap(str(img_file)).scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl.setPixmap(pix)
            lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            g_layout.addWidget(lbl)
        gallery.setWidget(container)
        layout.addWidget(gallery)

        # Details
        details = QLabel(
            f"<b>{self.listing['brand']} {self.listing['model']} ({self.listing['year']})</b><br>"
            f"Type: {self.listing['vehicle_type']} &nbsp; Fuel: {self.listing['fuel_type']}<br>"
            f"KM: {self.listing['total_km']}<br>"
            f"Available: {self.listing['from_date']} to {self.listing['to_date']}<br>"
            f"Price/Day: €{self.listing['price_per_day']:.2f}<br><br>"
            f"{self.listing['description']}"
        )
        details.setStyleSheet("font-size:16px; color:#444; margin:10px;")
        layout.addWidget(details)

        # Date selectors
        form = QHBoxLayout()
        self.from_date = QDateEdit(calendarPopup=True)
        self.from_date.setDate(QDate.currentDate())
        form.addWidget(QLabel("From:"))
        form.addWidget(self.from_date)
        self.to_date = QDateEdit(calendarPopup=True)
        self.to_date.setDate(QDate.currentDate().addDays(1))
        form.addWidget(QLabel("To:"))
        form.addWidget(self.to_date)
        layout.addLayout(form)

        # Total
        self.total_lbl = QLabel("Total: €0.00")
        self.total_lbl.setStyleSheet("font-size:20px; font-weight:bold; margin:10px;")
        layout.addWidget(self.total_lbl, alignment=Qt.AlignCenter)
        self.from_date.dateChanged.connect(self._update_total)
        self.to_date.dateChanged.connect(self._update_total)
        self._update_total()

        # Confirm
        btn = QPushButton("Confirm Booking")
        btn.setFixedSize(180, 50)
        btn.setStyleSheet(
            "QPushButton { background: skyblue; color: white; border-radius:8px;"
            " font-size:16px; } QPushButton:hover { background: deepskyblue; }"
        )
        btn.clicked.connect(self._confirm_booking)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

    def _customize_calendars(self):
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("lightgray"))
        fmt.setFontStrikeOut(True)
        for start, end in self.unavailable:
            day = start
            while day < end:
                qd = QDate(day.year, day.month, day.day)
                self.from_date.calendarWidget().setDateTextFormat(qd, fmt)
                self.to_date.calendarWidget().setDateTextFormat(qd, fmt)
                day += timedelta(days=1)

    def _update_total(self):
        s = self.from_date.date().toPyDate()
        t = self.to_date.date().toPyDate()
        days = (t - s).days
        if days <= 0:
            self.total_lbl.setText("Invalid date range")
            return
        self.total_lbl.setText(f"Total: €{days * self.listing['price_per_day']:.2f}")

    def _confirm_booking(self):
        s = self.from_date.date().toPyDate()
        t = self.to_date.date().toPyDate()
        days = (t - s).days
        if days <= 0:
            QMessageBox.warning(self, "Error", "Invalid date range.")
            return
        # overlap check
        for start, end in self.unavailable:
            if s < end and t > start:
                QMessageBox.critical(self, "Unavailable", "Car already booked in this period.")
                return
        total = days * self.listing['price_per_day']
        if self.user.balance < total:
            QMessageBox.critical(self, "Low Balance", "Insufficient balance.")
            return
        db = DB.Database()
        conn = db.connect()
        if not conn:
            QMessageBox.critical(self, "Error", "DB connection failed.")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO rents (user_who_rents, from_date, number_of_days, id_of_listing) VALUES (%s,%s,%s,%s)",
                (self.user.username, s.strftime('%Y-%m-%d'), days, self.listing['id'])
            )
<<<<<<< HEAD
=======
            cur.execute(
                "UPDATE user SET balance=balance-%s WHERE username=%s",
                (total, self.user.username)
            )
>>>>>>> Babis
            conn.commit()
            self.user.balance -= total
            QMessageBox.information(self, "Success", "Booking confirmed!")
            self.booking_confirmed.emit()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Booking failed: {e}")
        finally:
            conn.close()