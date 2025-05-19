from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QDateEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QDate
from screens.PhotosScreen import PhotosScreen

class CreateScreen(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Create Listing")
        self.setMinimumSize(300, 300)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Center frame
        frame = QFrame()
        frame.setStyleSheet("background: white; border-radius: 10px;")
        frame.setFixedWidth(400)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("Create Listing")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        frame_layout.addWidget(title)

        # Notification label (hidden by default)
        self.notify_label = QLabel("All fields are required")
        self.notify_label.setStyleSheet("color: red; font-weight: bold;")
        self.notify_label.setAlignment(Qt.AlignCenter)
        self.notify_label.hide()
        frame_layout.insertWidget(1, self.notify_label)  # Show below the title

        # Form
        form_layout = QFormLayout()

        # Style for input fields
        field_style = """
            QLineEdit, QTextEdit, QDateEdit {
                border: 1.5px solid #87ceeb;
                border-radius: 6px;
                padding: 6px;
                background: #f7fbff;
                font-size: 15px;
            }
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {
                border: 2px solid #4682b4;
                background: #e6f2fa;
            }
        """

        self.vehicle_type = QLineEdit()
        self.vehicle_type.setStyleSheet(field_style)
        self.brand = QLineEdit()
        self.brand.setStyleSheet(field_style)
        self.model = QLineEdit()
        self.model.setStyleSheet(field_style)
        self.year = QLineEdit()
        self.year.setStyleSheet(field_style)
        self.total_km = QLineEdit()
        self.total_km.setStyleSheet(field_style)
        self.fuel_type = QLineEdit()
        self.fuel_type.setStyleSheet(field_style)
        self.description = QTextEdit()
        self.description.setStyleSheet(field_style)
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate())
        self.from_date.setStyleSheet(field_style)
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setStyleSheet(field_style)

        form_layout.addRow("Vehicle Type:", self.vehicle_type)
        form_layout.addRow("Brand:", self.brand)
        form_layout.addRow("Model:", self.model)
        form_layout.addRow("Year:", self.year)
        form_layout.addRow("Total km:", self.total_km)
        form_layout.addRow("Fuel Type:", self.fuel_type)
        form_layout.addRow("Description:", self.description)
        form_layout.addRow("From Date:", self.from_date)
        form_layout.addRow("To Date:", self.to_date)

        frame_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 8px 24px;"
        )
        cancel_btn.clicked.connect(self.cancel)

        create_btn = QPushButton("Create")
        create_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 8px 24px;"
        )
        create_btn.clicked.connect(self.enterDetails)  # Use enterDetails as handler

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(create_btn)
        frame_layout.addLayout(button_layout)

        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        self.showMaximized()

    def cancel(self):
        self.close()

    def detailsNotify(self):
        self.notify_label.show()

    def checkDetails(self):
        # Check if all fields are filled
        if (
            not self.vehicle_type.text().strip() or
            not self.brand.text().strip() or
            not self.model.text().strip() or
            not self.year.text().strip() or
            not self.total_km.text().strip() or
            not self.fuel_type.text().strip() or
            not self.description.toPlainText().strip() or
            not self.from_date.date().isValid() or
            not self.to_date.date().isValid()
        ):
            self.detailsNotify()
        else:
            self.notify_label.hide()
            # Implementation for valid details will go here
            data = {
                "vehicle_type": self.vehicle_type.text(),
                "brand": self.brand.text(),
                "model": self.model.text(),
                "year": self.year.text(),
                "total_km": self.total_km.text(),
                "fuel_type": self.fuel_type.text(),
                "description": self.description.toPlainText(),
                "from_date": self.from_date.date().toString("yyyy-MM-dd"),
                "to_date": self.to_date.date().toString("yyyy-MM-dd"),
            }
            self.photos_screen = PhotosScreen(self.user, data)
            self.photos_screen.show()

    def enterDetails(self):
        self.checkDetails()