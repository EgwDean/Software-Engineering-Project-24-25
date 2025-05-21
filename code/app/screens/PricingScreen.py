from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import os
import shutil
import entities.VehicleListing as VL
from datetime import datetime

class PricingScreen(QWidget):
    def __init__(self, user, data, photos, parent=None):
        super().__init__(parent)
        self.user = user
        self.data = data
        self.photos = photos

        self.setWindowTitle("Pricing")
        self.setMinimumSize(400, 300)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Center frame
        frame = QFrame()
        frame.setStyleSheet("background: white; border-radius: 10px;")
        frame.setFixedWidth(400)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("Select Pricing")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        frame_layout.addWidget(title)

        # Price/Day field
        price_label = QLabel("Price/Day")
        price_label.setStyleSheet("font-size: 15px; margin-bottom: 4px;")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter price per day")
        self.price_input.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #87ceeb;
                border-radius: 6px;
                padding: 6px;
                background: #f7fbff;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #4682b4;
                background: #e6f2fa;
            }
        """)
        frame_layout.addWidget(price_label)
        frame_layout.addWidget(self.price_input)

        # Notification label (hidden by default)
        self.notify_label = QLabel("please enter a valid price")
        self.notify_label.setStyleSheet("color: red; font-weight: bold;")
        self.notify_label.setAlignment(Qt.AlignCenter)
        self.notify_label.hide()
        frame_layout.addWidget(self.notify_label)

        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 8px 24px;"
        )
        cancel_btn.clicked.connect(self.cancel)

        finalize_btn = QPushButton("Finalize")
        finalize_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 8px 24px;"
        )
        finalize_btn.clicked.connect(self.enterPricing)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(finalize_btn)
        frame_layout.addLayout(button_layout)

        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        self.showMaximized()

    def pricingNotify(self):
        self.notify_label.show()

    def enterPricing(self):
        self.checkPricing()

    def checkPricing(self):
        price_text = self.price_input.text().strip()
        try:
            price = float(price_text)
            if price <= 0:
                raise ValueError
        except ValueError:
            self.pricingNotify()
            return

        self.notify_label.hide()

        # Move images from temp to images folder
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # .../code
        temp_dir = os.path.join(base_dir, "assets", "temp")
        images_dir = os.path.join(base_dir, "assets", "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        saved_photos = []
        for photo_path in self.photos:
            if os.path.isfile(photo_path):
                filename = os.path.basename(photo_path)
                dest_path = os.path.join(images_dir, filename)
                shutil.move(photo_path, dest_path)
                saved_photos.append(dest_path)
        # Empty temp folder
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        # Prepare data for VehicleListing
        # Convert date fields to MySQL DATE format (YYYY-MM-DD)
        def to_mysql_date(date_str):
            # Accepts 'yyyy-MM-dd' or similar, returns 'YYYY-MM-DD'
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
            except Exception:
                return date_str  # fallback, but should be correct

        from_date = to_mysql_date(self.data.get("from_date", ""))
        to_date = to_mysql_date(self.data.get("to_date", ""))

        listing_data = {
            "name_of_user": self.user.username,
            "price_per_day": price,
            "vehicle_type": self.data.get("vehicle_type"),
            "brand": self.data.get("brand"),
            "model": self.data.get("model"),
            "year": self.data.get("year"),
            "total_km": self.data.get("total_km"),
            "fuel_type": self.data.get("fuel_type"),
            "description": self.data.get("description"),
            "from_date": from_date,
            "to_date": to_date,
            "status": "listed"
        }

        # Create and store VehicleListing
        try:
            vehicle_listing = VL.VehicleListing(None)  # id will be auto-incremented
            result = vehicle_listing.store(
                listing_data["name_of_user"],
                listing_data["price_per_day"],
                listing_data["vehicle_type"],
                listing_data["brand"],
                listing_data["model"],
                listing_data["year"],
                listing_data["total_km"],
                listing_data["fuel_type"],
                listing_data["description"],
                listing_data["from_date"],
                listing_data["to_date"],
                listing_data["status"]
            )
            if result:
                QMessageBox.information(self, "Success", "Listing created successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to create listing.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        self.close()

    def cancel(self):
        self._should_empty_temp = True
        self.close()

    def closeEvent(self, event):
        # Only empty temp if self._should_empty_temp is True (set by cancel or X)
        if getattr(self, "_should_empty_temp", False):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # .../code
            temp_dir = os.path.join(base_dir, "assets", "temp")
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
        super().closeEvent(event)