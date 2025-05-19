from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
import os
import shutil

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
        # finalize_btn.clicked.connect(self.finalize)  # To be implemented

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(finalize_btn)
        frame_layout.addLayout(button_layout)

        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        self.showMaximized()

    def cancel(self):
        self.close()

    def closeEvent(self, event):
        # Empty the temp folder in code/assets/temp when window is closed
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