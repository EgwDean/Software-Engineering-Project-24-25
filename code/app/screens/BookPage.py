from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame,
    QDateEdit, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QPixmap
from datetime import datetime
import services.Database as DB
from pathlib import Path

class BookPage(QWidget):
    back_requested = pyqtSignal()
    booking_confirmed = pyqtSignal()

    def __init__(self, user, listing):
        super().__init__()
        self.user = user
        self.listing = listing
        self.setWindowTitle("Book Listing")
        self.setStyleSheet("background-color: #f5f5f5;")
        self.showMaximized()
        self.image_path = Path(__file__).parent.parent.parent / 'assets' / 'images' / f"img_{self.listing['id']}_1.jpg"
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Top bar with balance and back button
        top_bar = QHBoxLayout()

        back_btn = QPushButton("←")
        back_btn.setFixedSize(40, 40)
        back_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: skyblue; font-size: 37px; }"
            "QPushButton:hover { color: deepskyblue; }"
        )
        back_btn.clicked.connect(self.back_requested.emit)
        top_bar.addWidget(back_btn, alignment=Qt.AlignLeft)

        top_bar.addStretch()
        balance_label = QLabel(f"Balance: €{self.user.balance:.2f}")
        balance_label.setStyleSheet("font-size: 18px; color: #333; padding: 10px;")
        top_bar.addWidget(balance_label, alignment=Qt.AlignRight)

        layout.addLayout(top_bar)

        # Image
        img_label = QLabel()
        pixmap = QPixmap(str(self.image_path)).scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_label.setPixmap(pixmap)
        img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(img_label)

        # Vehicle details
        details = QLabel(
            f"<b>{self.listing['brand']} {self.listing['model']} ({self.listing['year']})</b><br>"
            f"Type: {self.listing['vehicle_type']}<br>"
            f"Fuel: {self.listing['fuel_type']}<br>"
            f"KM: {self.listing['total_km']}<br>"
            f"Available: {self.listing['from_date']} to {self.listing['to_date']}<br>"
            f"Price/Day: €{self.listing['price_per_day']:.2f}<br><br>"
            f"<i>{self.listing['description']}</i>"
        )
        details.setStyleSheet("font-size: 18px; color: #444;")
        layout.addWidget(details)

        # Booking form
        form = QHBoxLayout()

        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate())
        self.from_date.dateChanged.connect(self._update_total)

        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate().addDays(1))
        self.to_date.dateChanged.connect(self._update_total)

        form.addWidget(QLabel("From: "))
        form.addWidget(self.from_date)
        form.addWidget(QLabel("To: "))
        form.addWidget(self.to_date)
        layout.addLayout(form)

        # Total cost
        self.total_label = QLabel("Total: €0.00")
        self.total_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #000; margin: 10px;")
        layout.addWidget(self.total_label, alignment=Qt.AlignCenter)

        self._update_total()

        # Confirm button
        confirm_btn = QPushButton("Confirm Booking")
        confirm_btn.setFixedSize(200, 50)
        confirm_btn.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; font-size: 18px;"
            " border: none; border-radius: 10px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        confirm_btn.clicked.connect(self._confirm_booking)
        layout.addWidget(confirm_btn, alignment=Qt.AlignCenter)

    def _update_total(self):
        start = self.from_date.date().toPyDate()
        end = self.to_date.date().toPyDate()
        days = (end - start).days
        if days <= 0:
            self.total_label.setText("Invalid date range")
            return
        total_cost = days * float(self.listing['price_per_day'])
        self.total_label.setText(f"Total: €{total_cost:.2f}")

    def _confirm_booking(self):
        start = self.from_date.date().toPyDate()
        end = self.to_date.date().toPyDate()
        days = (end - start).days

        if days <= 0:
            QMessageBox.warning(self, "Invalid", "Please choose a valid date range.")
            return

        total_cost = days * float(self.listing['price_per_day'])

        if self.user.balance < total_cost:
            QMessageBox.critical(self, "Low Balance", "You do not have enough balance.")
            return

        db = DB.Database()
        conn = db.connect()
        if not conn:
            QMessageBox.critical(self, "Error", "Database connection failed.")
            return

        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO rents (user_who_rents, from_date, number_of_days, id_of_listing) VALUES (%s, %s, %s, %s)",
                (self.user.username, start.strftime('%Y-%m-%d'), days, self.listing['id'])
            )
            new_balance = self.user.balance - total_cost
            cur.execute(
                "UPDATE user SET balance = %s WHERE username = %s",
                (new_balance, self.user.username)
            )
            conn.commit()
            self.user.balance = new_balance
            QMessageBox.information(self, "Success", "Booking confirmed!")
            self.booking_confirmed.emit()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Booking failed: {e}")
        finally:
            conn.close()
