from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import shutil
from screens.PricingScreen import PricingScreen

class CompletionScreen(QWidget):
    def __init__(self, user, data, photos, parent=None):
        super().__init__(parent)
        self.user = user
        self.data = data
        self.photos = photos

        self.setWindowTitle("Completion")
        self.setMinimumSize(400, 300)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Center frame
        frame = QFrame()
        frame.setStyleSheet("background: white; border-radius: 10px;")
        frame.setFixedWidth(500)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("Complete Creation")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        frame_layout.addWidget(title)

        # Data display
        for key, value in self.data.items():
            label = QLabel(f"<b>{key.replace('_', ' ').title()}:</b> {value}")
            label.setStyleSheet("font-size: 15px; margin-bottom: 4px;")
            frame_layout.addWidget(label)

        # Photos display (scrollable if many)
        photos_label = QLabel("Photos:")
        photos_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        frame_layout.addWidget(photos_label)

        photos_scroll = QScrollArea()
        photos_widget = QWidget()
        photos_layout = QHBoxLayout(photos_widget)

        for photo_path in self.photos:
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label = QLabel()
                img_label.setPixmap(pixmap)
                img_label.setFixedSize(100, 100)
                photos_layout.addWidget(img_label)

        photos_scroll.setWidget(photos_widget)
        photos_scroll.setWidgetResizable(True)
        photos_scroll.setFixedHeight(120)
        frame_layout.addWidget(photos_scroll)

        # Complete and Cancel buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 10px 24px; margin-top: 20px;"
        )
        cancel_btn.clicked.connect(self.cancel)

        complete_btn = QPushButton("Complete")
        complete_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 10px 24px; margin-top: 20px;"
        )
        complete_btn.clicked.connect(self.open_pricing_screen)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(complete_btn)
        frame_layout.addLayout(button_layout)

        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        self.showMaximized()

    def cancel(self):
        self._should_empty_temp = True
        self.close()

    def closeEvent(self, event):
        # Only empty temp if self._should_empty_temp is True (set by cancel or X)
        if getattr(self, "_should_empty_temp", False):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

    def open_pricing_screen(self):
        self.pricing_screen = PricingScreen(self.user, self.data, self.photos)
        self.pricing_screen.show()
        self.close()