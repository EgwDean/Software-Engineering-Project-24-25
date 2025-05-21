from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt

class SubscriptionScreen(QWidget):
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Subscription")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.showMaximized()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setAlignment(Qt.AlignTop)

        # Top frame (mimic CreateScreen)
        top_frame = QFrame()
        top_frame.setStyleSheet("background-color: skyblue; border-radius: 10px;")
        top_layout = QVBoxLayout()
        title_label = QLabel("Subscription Screen")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #333; padding: 20px;")
        top_layout.addWidget(title_label)
        top_frame.setLayout(top_layout)
        main_layout.addWidget(top_frame)

        # Placeholder for future subscription content
        placeholder_label = QLabel("Subscription Screen (to be implemented)")
        placeholder_label.setStyleSheet("font-size: 18px; color: #555; margin-top: 40px;")
        main_layout.addWidget(placeholder_label)

        self.setLayout(main_layout)